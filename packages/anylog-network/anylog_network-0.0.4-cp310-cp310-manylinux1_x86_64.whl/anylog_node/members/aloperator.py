'''
By using this source code, you acknowledge that this software in source code form remains a confidential information of AnyLog, Inc.,
and you shall not transfer it to any other party without AnyLog, Inc.'s prior written consent. You further acknowledge that all right,
title and interest in and to this source code, and any copies and/or derivatives thereof and all documentation, which describes
and/or composes such source code or any such derivatives, shall remain the sole and exclusive property of AnyLog, Inc.,
and you shall not edit, reverse engineer, copy, emulate, create derivatives of, compile or decompile or otherwise tamper or modify
this source code in any way, or allow others to do so. In the event of any such editing, reverse engineering, copying, emulation,
creation of derivative, compilation, decompilation, tampering or modification of this source code by you, or any of your affiliates (term
to be broadly interpreted) you or your such affiliates shall unconditionally assign and transfer any intellectual property created by any
such non-permitted act to AnyLog, Inc.
'''
import anylog_node.cmd.member_cmd as member_cmd
import anylog_node.generic.process_status as process_status
import anylog_node.generic.process_log as process_log
import anylog_node.generic.interpreter as interpreter
import anylog_node.json_to_sql.map_json_to_insert as map_json_to_insert
import anylog_node.generic.utils_io as utils_io
import anylog_node.generic.utils_data as utils_data
import anylog_node.generic.utils_json as utils_json
import anylog_node.generic.utils_print as utils_print
import anylog_node.dbms.db_info as db_info
import anylog_node.generic.utils_columns as utils_columns
import anylog_node.tcpip.net_utils as net_utils
import anylog_node.generic.utils_queue as utils_queue
import anylog_node.generic.params as params
import anylog_node.dbms.partitions as partitions
import anylog_node.blockchain.metadata as metadata
from anylog_node.generic.streaming_data import flush_buffered_data
import anylog_node.dbms.create_table as create_table
import anylog_node.generic.utils_threads as utils_threads
import anylog_node.generic.utils_monitor as utils_monitor

mem_view = None

meta_info_sql_ = None  # A dictionary with info on the sql files processed
meta_info_json_ = None  # A dictionary with info on the json files processed


is_running = False
on_wait = False  # waiting for blockchain
err_stamp = 0  # used to make sure that error files do not get the same timestamo


cmd_get_operator = ["blockchain", "get", "operator", "where", "ip", "=", None, "and", "port", "=", None, "bring.first"]


error_info_ = None      # A list with info on errors while processing data
current_config = None  # A ptr to the configuration values so it can e printed

status_info = [
    "Cluster Member: False, Using Master: {A1}, Threads Pool: {A2}",
    "Cluster Member: True, Using Master: {A1}, Threads Pool: {A2}",
]

status_queue_ = utils_queue.MsgQueue(0)
status_queue_.set_static_queue(status_info)

start_time = utils_columns.get_current_time_in_sec()   # the time the operator node started

statistics_ = {}

file_info_objects_ = {}     # Maintain file_info object for every participating thread

operator_pool_ = None       # Workers threads

first_file_time_ = 0        # Time first file is processed
last_file_time_ = 0
main_config_ = None          # The configuration of operator

class OperatorConfig:
    def __init__(self):
        self.master_node = None
        self.company = None
        self.platform = "local"         # The default platform, can be changed to master or blockchain

        self.is_create_table = False

        self.blockchain_file = None

        self.watch_dir = None
        self.err_dir = None
        self.bkup_dir = None
        self.distr_dir = None
        self.archive_dir = None

        self.is_archive = False
        self.is_distributor = False

        self.json_move_dir = False
        self.json_is_move = False
        self.json_is_compress = False
        self.json_is_delete = False

        self.sql_is_delete = False
        self.sql_is_compress = False
        self.sql_is_move = False

    def is_with_distributor(self):
        return self.is_distributor


# ----------------------------------------------------------
# Test configuration value
# ----------------------------------------------------------
def is_with_distributor():
    global main_config_
    if main_config_:
        ret_val = main_config_.is_with_distributor()
    else:
        ret_val = False
    return ret_val
# ----------------------------------------------------------
# Process of an operator
# connect dbms psql !db_user !db_port lsl_demo
# partition lsl_demo * using timestamp by month
# partition lsl_demo ping_sensor using timestamp by 7 days
# run operator where create_table = true and compress_sql = true and compress_json = true
# run operator where create_table = true and compress_sql = true and compress_json = true and blockchain = true
# run operator where create_table = true and compress_sql = true and compress_json = true and master_node =  10.0.0.5:2048

# Use tsd_info table
# connect dbms sqlite !db_user !db_port almgm
# run operator where create_table = true and compress_sql = true and compress_json = true and update_tsd_info = true
# run operator where create_table = true and compress_sql = true and compress_json = true
# ----------------------------------------------------------
def run_operator(dummy: str, conditions: dict):
    global main_config_
    global mem_view
    global is_running
    global on_wait
    global error_info_      # Info on errors while processing files
    global current_config
    global start_time
    global meta_info_sql_
    global meta_info_json_
    global operator_pool_
    global first_file_time_
    global last_file_time_

    process_status.reset_exit("operator")

    meta_info_sql_ = {}  # A dictionary with info on the sql files processed
    meta_info_json_ = {}  # A dictionary with info on the json files processed

    error_info_ = [  # info on errors while processing data files
        # Counter       Last        Last        Last    Last
        # Files to      DBMS        Table       Error   Error
        # Error         Name        Name        Code    Message
        ["Duplicate JSON Files", 0, "", "", 0, ""],  # A counter for duplicate JSON Files
        ["JSON Files Errors", 0, "", "", 0, ""],  # JSON files processed with error
        ["SQL Files Errors", 0, "", "", 0, ""]  # SQL files processed with error
    ]

    start_time = utils_columns.get_current_time_in_sec()  # the time the operator node started

    current_config = conditions

    config = OperatorConfig()
    main_config_ = config       # Make the config public

    status = process_status.ProcessStat()

    config.watch_dir = interpreter.get_one_value(conditions, "watch_dir")
    config.err_dir = interpreter.get_one_value(conditions, "err_dir")
    config.bkup_dir = interpreter.get_one_value(conditions, "bkup_dir")

    file_types = conditions["file_type"]  # get the list of file types to consider

    par_section = 2  # section 2 in the .SQL file shows the partition ID - Only relevant for SQL file which is organized from the JSON file

    config.blockchain_file = interpreter.get_one_value(conditions, "blockchain_file")

    # Get the platform - the default is "local"
    config.master_node = interpreter.get_one_value(conditions, "master_node")
    if config.master_node:
        config.platform = "master"
    else:
        is_blockchain = interpreter.get_one_value(conditions, "blockchain")
        if is_blockchain:
            config.platform = "blockchain"

    config.company_name = interpreter.get_one_value(conditions, "company")

    config.is_create_table =  interpreter.get_one_value_or_default(conditions, "create_table", True)

    config.json_is_delete = interpreter.get_one_value_or_default(conditions, "delete_json", False)  # The default is place in backup

    config.json_move_dir = interpreter.get_one_value(conditions, "bkup_dir")
    config.json_is_compress = interpreter.get_one_value(conditions, "compress_json")
    config.json_is_move = interpreter.get_one_value(conditions, "move_json")

    # If distributor is True, Move JSON file to !distr_dir
    distributor = interpreter.get_one_value_or_default(conditions, "distributor", False)
    if distributor:
        config.is_distributor = True
        config.distr_dir = interpreter.get_one_value(conditions, "distr_dir")

    if interpreter.get_one_value(conditions, "archive"):
        # Move data to archive
        config.is_archive = True
        config.archive_dir = interpreter.get_one_value(conditions, "archive_dir")
        config.json_is_compress = True
        config.json_is_move = True

    if not config.archive_dir:
        config.archive_dir = params.get_value_if_available("!archive_dir")


    config.sql_is_delete = interpreter.get_one_value_or_default(conditions, "delete_sql", True)   # The default is delete

    if config.sql_is_delete:
        config.sql_is_compress = False
        config.sql_is_move = False
    else:
        config.sql_is_compress = interpreter.get_one_value(conditions, "compress_sql")
        config.sql_is_move = True

    # Update a summary table (tsd_info table in almgm dbms) evry time a file is loaded
    if interpreter.get_one_value(conditions, "update_tsd_info"):
        with_tsd_info = True
    else:
        with_tsd_info = False

    if not mem_view:
        data_buffer = bytearray(params.TCP_BUFFER_SIZE)
        mem_view = memoryview(data_buffer)  # not using one instance as it may be overwritten before message send

    flush_streaming = interpreter.get_one_value_or_default(conditions, "flush_streaming", False)  # The default is use cluster
    if flush_streaming:
        # this operator thread will flush streaming data to files (if the streamer is not configured)
        flush_function = flush_buffered_data
    else:
        flush_function = None

    is_running = True



    stat_reset()            # Reset the statistics available to thee "get operator stat"

    create_table.set_generic_params(True, config)       # Make the operator params available to the create table process

    threads_count = interpreter.get_one_value_or_default(conditions, "threads", 1)
    if threads_count > 1:
        operator_pool_ = utils_threads.WorkersPool("Operator Pool", threads_count)
        # files_in_process is a dictionary of files which are currently being processed
        # The list is maintained to avoid the same file provided to a different thread
        files_in_process = {}
    else:
        operator_pool_ = None
        files_in_process = None
    status_info[0] = status_info[0].replace("{A2}", str(threads_count))
    status_info[1] = status_info[1].replace("{A2}", str(threads_count))

    for task_id in range (threads_count):
        file_info_objects_[task_id] = utils_io.FileMetadata()       # save file_info object as f(thread_id)


    while 1:

        file_list = []  # needs to be inside the while loop to be initiated (as the same file will be called again)

        ret_val, files_to_process = member_cmd.get_files_from_dir(status, "operator", 5, config.watch_dir, "file", file_types, file_list, flush_function, files_in_process, True)

        if ret_val:
            # Including Operator terminated - or global termination
            break

        if not first_file_time_:
            # set the time of the first file processing
            last_file_time_ = utils_columns.get_current_time_in_sec()
            first_file_time_ =last_file_time_


        for file_name in files_to_process:

            if threads_count == 1:
                file_info = file_info_objects_[0]
                ret_val, new_name, row_id = prepare_file(status, config, with_tsd_info, file_info, file_name)
                if ret_val:
                    if ret_val < process_status.NON_ERROR_RET_VALUE:
                        ret_val = file_processing_failure(status, ret_val, config, new_name, file_info)
                        if ret_val:
                            break    # File moved to err dir failed - exit
                        # moved to error dir - get next file
                    else:
                        # The dbms and TSD tables were updated in write_immediate
                        ret_val = process_status.SUCCESS    # ret_val indicated 'write immediate' - not an error
                    continue

                ret_val = process_watch_file(status, mem_view, conditions, config, with_tsd_info, par_section, file_info, row_id)
            else:

                task = operator_pool_.get_free_task()
                task_id = task.get_task_id()

                file_info = file_info_objects_[task_id]
                ret_val, new_name, row_id = prepare_file(status, config, with_tsd_info, file_info, file_name)
                if ret_val:
                    # The ret_val can represent PROCESSED_IMMEDIATE
                    # Whereas the dbms and TSD tables were updated
                    operator_pool_.ignore_task(task)       # Return the unused task to the ree list
                    if ret_val < process_status.NON_ERROR_RET_VALUE:
                        ret_val = file_processing_failure(status, ret_val, config, new_name, file_info)
                        if ret_val:
                            break    # File moved to err dir failed - exit
                    else:
                        ret_val = process_status.SUCCESS    # ret_val indicated 'write immediate' - not an error
                    continue     # File moved to error dir - get next file

                # Test that the first file of the table was updated - such that the table was created, avoiding race conditions
                if is_table_created(file_info):     # This setup avoids race condition between threads to create the table
                    # The table was created - take a thread from the pool and process the file
                    files_in_process[file_info.get_no_path_name()] = True      # Flag that the file is provided to a thread for processing
                    task.set_cmd(process_watch_file, [conditions, config, with_tsd_info, par_section, file_info, row_id])
                    operator_pool_.add_new_task(task)       # Process the task + return to the free list after the process
                else:
                    # FIRST UPDATE - Use current thread
                    operator_pool_.ignore_task(task)  # Return the unused task to the ree list

                    ret_val = process_watch_file(status, mem_view, conditions, config, with_tsd_info, par_section, file_info, row_id)
                    if ret_val:
                        break

                if len(files_in_process) > 100:
                    # remove file names which were processed
                    ret_val, files_list = utils_io.get_files_from_dir(status, config.watch_dir, None, file_types)
                    if ret_val:
                        break
                    # go over all files in the directory, and create a new dictionary with the relevant  files
                    disk_files_in_process = {}
                    for file_on_disk in files_list:
                        if file_on_disk in files_in_process:
                            # this file is in process
                            disk_files_in_process[file_on_disk] = True  # Flag that the file is currently processed
                    files_in_process = disk_files_in_process

        last_file_time_ = utils_columns.get_current_time_in_sec()
        if ret_val:
            break

    process_log.add_and_print("event", "Operator process terminated: %s" % process_status.get_status_text(ret_val))

    if threads_count > 1:
        operator_pool_.exit()        # Will make the threads to exit
        operator_pool_ = None

    create_table.set_generic_params(False, None)  # Disable operator params for the create table process

    is_running = False

    current_config = False
# ----------------------------------------------------------
# This setup avoids race condition between threads to create the table:
# If the table is not created - we revert to a single thread process.
# A table is created by considering it was processed successfully at least once
# ----------------------------------------------------------
def is_table_created(file_info):

    global meta_info_json_       # Stats on SQL files
    global meta_info_sql_        # Stats on partitions

    ret_val = False
    table_key = file_info.dbms_name + '.' + file_info.table_name

    if file_info.get_file_type() == "json":
        # Test dbms name + table name
        if table_key in meta_info_json_:
            ret_val = True          # Was processed
    else:
        # SQL file - consider partition
        par_name = file_info.get_partition_name()
        if par_name:
            table_key += ("." + file_info.get_partition_name())
        if table_key in meta_info_sql_:
            ret_val = True          # Partition Was processed
    return ret_val
# ----------------------------------------------------------
# Prepare the file for processing
# ----------------------------------------------------------
def prepare_file(status, config, with_tsd_info, file_info, file_name):


    ret_val, cluster_id, member_id = get_metadata_info(status)


    new_name = file_name
    row_id = '0'        # The row ID in the TSD table associated with the JSON file

    if ret_val:
        return [ret_val, new_name, row_id]

    ret_val = file_info.set_file_name_metadata(status, file_name)


    if not ret_val:

        if file_info.tsd_member == '@':
            # This is a file from the streaming process with write immediate flag set to True.
            # The data already updated the local tables.
            # --> Move the file to archive or distributor
            update_stats(meta_info_json_, file_info.dbms_name + '.' + file_info.table_name, True, True)
            ret_val = move_processed_json_file(status, config, file_info, member_id, file_name)

            if not ret_val:
                ret_val = process_status.PROCESSED_IMMEDIATE

            return [ret_val, new_name, row_id]  # Can return success or error

        if not db_info.is_dbms(file_info.dbms_name):
            status.add_error("Operator is not connected to dbms: '%s'" % file_info.dbms_name)
            ret_val = process_status.ERR_dbms_not_opened
            return [ret_val, new_name, row_id]

        if file_info.get_file_type() == "json":

            if with_tsd_info:
                if not file_info.with_hash_value():
                    ret_val = file_info.add_hash_value(status, file_info.dbms_name, file_info.table_name)  # calculate the file hash value to include in the file name
                else:
                    ret_val = process_status.SUCCESS

                if not ret_val:
                    # Rename the file to include the hash value
                    # Test the Hash value is unique and  rename the file to include the metadata components.
                    # The metadata includes the Row ID + the row ID is updated into the INSERT statements
                    ret_val, was_renamed, new_name, row_id = tsd_table_process(status, file_info, member_id)

                    if not ret_val:
                        if was_renamed:
                            # Replace to the new file name (regardless if success of failure)
                            ret_val = file_info.set_file_name_metadata(status, new_name)

    return [ret_val, new_name, row_id]



# ----------------------------------------------------------
# Process a single file
# ----------------------------------------------------------
def process_watch_file(status, mem_view, conditions, config, with_tsd_info, par_section, file_info, row_id):
    '''
    status - status object
    mem_view - IO buffer
    conditions - users params
    config - derived params
    with_tsd_info - determines if TSD tables are updated
    par_section - the section with the partition name (should be 2 - after table name)
    file_info - an object with derived info to determine file name info
    row_id - the TSD table row ID to update
    files_in_process - a dictionary with file names that are currently processed by the operator workers threads (if enabled)
    '''

    global file_info_objects_
    global meta_info_json_

    file_name = file_info.get_file_name()

    ret_val, cluster_id, member_id = get_metadata_info(status)
    if not ret_val:

        trace_level = member_cmd.commands["run operator"]['trace']

        if ret_val:
            status.add_error("Operator failed to retrieve dbms name and table name from file: '%s'" % file_name)
            process_file = False
        else:

            if trace_level > 1:
                utils_print.output("\r\n[Operator] [New File] [" + file_info.file_name + "]", True)

            process_file = True
            if "limit_tables" in conditions.keys():
                # only listed tables are allowed
                table_key = file_info.dbms_name + '.' + file_info.table_name
                if table_key not in conditions["limit_tables"]:
                    status.add_error("Operator retrieved a file which fails to satisfy 'limit_tables': '%s'" % file_name)
                    ret_val = process_status.Table_excluded
                    process_file = False

            if not db_info.is_dbms(file_info.dbms_name):
                status.add_error("Operator is not connected to dbms: '%s'" % file_info.dbms_name)
                ret_val = process_status.ERR_dbms_not_opened
                process_file = False
            else:

                if file_info.tsd_member == '@':
                    # This is a file from the streaming process with write immediate flag set to True.
                    # The data already updated the local tables.
                    # --> Move the file to archive or distributor
                    update_stats(meta_info_json_, file_info.dbms_name + '.' + file_info.table_name, True, True)
                    ret_val = move_processed_json_file(status, config, file_info, member_id, file_name)

                    return ret_val      # Can return success or error

                # Create the table if it does not exists - This process is done for every processed file (SQL or JSON)
                ret_val = create_table.validate_table(status, mem_view, file_info.dbms_name, file_info.table_name,
                                                      with_tsd_info, file_info.instructions, False, "", file_name,
                                                      trace_level)
                if ret_val:
                    process_file = False
                else:
                    # assign the table to the operator or to a cluster
                    ret_val = assign_table(status, cluster_id, config, file_info.dbms_name, file_info.table_name,
                                           trace_level)
                    if ret_val:
                        process_file = False
                    elif file_info.file_type == "json" and file_info.tsd_member:
                        # Test if the data is from a member of the cluster
                        if not metadata.test_cluster_member(cluster_id, file_info.tsd_member):
                            status.add_error("File received from member #%u which is not a member of the cluster: '%s'" % (
                            file_info.tsd_member, file_name))
                            ret_val = process_status.File_from_unrecognized_member
                            process_file = False

            if process_file:

                if file_info.file_type == "json":
                    # Rename the JSON File to the convention, add hash value to name

                    ret_val, process_file = process_json(status, config, file_info, with_tsd_info, member_id, row_id)
                    if trace_level:
                        utils_print.output("[Operator] [process JSON] [%s]" % process_status.get_status_text(ret_val), True)

                elif file_info.file_type == "sql":
                    ret_val, process_file = process_sql(status, cluster_id, config, file_info, par_section, with_tsd_info,
                                                        trace_level)
                    if trace_level:
                        utils_print.output("[Operator] [process SQL] [%s]" % process_status.get_status_text(ret_val), True)

                elif file_info.file_type == "gz":
                    # Onlu unzip the file
                    utils_io.uncompress_del_rename(status, file_name, file_info.file_name[:-3], config.err_dir)
                    return process_status.SUCCESS
                else:
                    process_log.add_and_print("event", "Operator requested to process non-supported file: %s" % file_name)
                    return process_status.Wrong_file_type



        if not process_file:
            ret_val = file_processing_failure(status, ret_val, config, file_name, file_info)


    return ret_val

# ----------------------------------------------------------
# Error in processing a file - update statistics and move to error directory
# Error is returned if file was not moved to error directory
# ----------------------------------------------------------
def file_processing_failure(status, error_code, config, file_name, file_info):
    # Move file to error dir and continue
    # file was not processed -> move to err dir
    global last_file_time_

    if file_info.get_file_type() == "json":
        if error_code == process_status.Duplicate_JSON_File:
            error_info_[0][1] += 1  # count the number of duuplicate JSON files (failed insert to tsd_info)
            error_info_[0][2] = file_info.dbms_name
            error_info_[0][3] = file_info.table_name
        else:
            error_info_[1][1] += 1  # count the number of JSON files placed in error dir
            error_info_[1][2] = file_info.dbms_name
            error_info_[1][3] = file_info.table_name
            error_info_[1][4] = error_code  # Keep last JSON error
    else:
        error_info_[2][1] += 1  # count the number of SQL files placed in error dir
        error_info_[2][2] = file_info.dbms_name
        error_info_[2][3] = file_info.table_name
        error_info_[2][4] = error_code  # Keep last SQL error

    if not utils_io.file_to_dir(status, config.err_dir, file_name, "err_%u" % error_code, True):
        ret_val = process_status.File_move_failed
    else:
        ret_val = process_status.SUCCESS

    last_file_time_ = utils_columns.get_current_time_in_sec()
    return ret_val

# ----------------------------------------------------------
# Get info from the metadata layer
# ----------------------------------------------------------
def get_metadata_info(status):

    global status_queue_

    cluster_id = '0'
    member_id = 0  # Without  a cluster

    # Load the metadata (only if the metadata was changed)
    ret_val = member_cmd.blockchain_load(status, ["blockchain", "get", "cluster"], False, 0)
    if ret_val:
        if ret_val == process_status.Needed_policy_not_available:
            # No cluster info
            status_queue_.set_index(0)  # Message: "Operator is not a member of a cluster"
            ret_val = process_status.SUCCESS
    else:
        cluster_id = metadata.get_node_cluster_id()  # A cluster ID associated with this node
        member_id = metadata.get_node_member_id()  # The ID of this node in the cluster
        if member_id:
            status_queue_.set_index(1)          # Message: "Operator is a member of a cluster"
        else:
            status_queue_.set_index(0)          # Message: "Operator is not a member of a cluster"


    return [ret_val, cluster_id, member_id]

# ----------------------------------------------------------
# process SQL File
# ----------------------------------------------------------
def process_sql(status, cluster_id, config, file_info, par_section, with_tsd_info, trace_level):

    global meta_info_sql_

    ret_val = process_status.SUCCESS
    process_file = True
    if partitions.is_partitioned(file_info.dbms_name, file_info.table_name):
        # Test if the partitioned table declared -> if not -> declare partitioned table
        if not par_section:
            status.add_error("Operator error: Missing 'par_name' definition to extract partition from file name")
            ret_val = process_status.Missing_configuration
        else:
            par_name = utils_io.get_section_name(file_info.file_name, par_section)
            if not par_name:
                # This is a partitioned table but file name has no partition ID
                status.add_error("Operator error: Failed to retrieve partition from file name: '%s'" % file_info.file_name)
                ret_val = process_status.Missing_par_in_file_name
                process_file = False
            else:
                ret_val = create_table.validate_table(status, mem_view, file_info.dbms_name, file_info.table_name,
                                      with_tsd_info, file_info.instructions, True, par_name, file_info.file_name, trace_level)
                if ret_val:
                    process_file = False
                else:
                    # assign the table to the operator or to a cluster
                    ret_val = assign_table(status, cluster_id, config, file_info.dbms_name, file_info.table_name, trace_level)
                    if ret_val:
                        process_file = False

    if not ret_val:
        ret_code, rows_counter = process_sql_file(status, config, file_info.dbms_name,
                         file_info.table_name, file_info.file_name)

        if ret_code:
            # SQL file was processed with no errors
            table_key = file_info.dbms_name + '.' + file_info.table_name
            par_name = file_info.get_partition_name()
            if par_name and par_name != '0':
                table_key += ("." + file_info.get_partition_name())
            update_stats(meta_info_sql_, table_key, False, False)
        else:
            process_file = False
            ret_val = process_status.ERR_SQL_failure


    return [ret_val, process_file]

# ----------------------------------------------------------
# 1) Create table
# 2) update TSD
# 3) Rename file
# 4) Make SQL file
# ----------------------------------------------------------
def process_json(status, config, file_info, with_tsd_info, member_id, row_id):
    '''
    row_id is the TSD Table Row which is to be updated
    '''

    ret_val = process_status.SUCCESS
    process_file = True

    if not ret_val:
        # Map to SQL, then compress or delete the file
        ret_val, sql_file_name, rows_count = process_json_file(status, config, file_info, member_id)

        if not ret_val:
            if with_tsd_info:
                if file_info.is_from_cluster_member(member_id):
                    # use TSD table of a member node in the cluster
                    tsd_table_name = "tsd_%u" % file_info.tsd_member
                    tsd_info_updated = False
                else:
                    # use TSD table of the current node (tsd_info)
                    tsd_table_name = "tsd_info"
                    tsd_info_updated = True         # Data from devices
                db_info.tsd_update_rows(status, tsd_table_name, int(row_id), rows_count)  # Update the number of rows on the JSON file
            else:
                tsd_info_updated = False # No HA processes
            # JSON file was processed with no errors
            update_stats(meta_info_json_, file_info.dbms_name + '.' + file_info.table_name, False, tsd_info_updated)

            stat_new_events(rows_count)     # Update the statistics on rows processed
        else:
            process_file = False


    return [ret_val, process_file]

# ----------------------------------------------------------
# Update the TSD table:
# 1) depending if file from device or from a member to the cluster
# 2) Update the TSD table
# 3) Rename file to reflect member
# ----------------------------------------------------------
def tsd_table_process(status, file_info, member_id):

    if file_info.tsd_member:
        # a file from a cluster member
        ret_val = process_status.SUCCESS
        tsd_member = file_info.tsd_member
    else:
        # A file from a sensor
        row_id = db_info.tsd_row_id_select(status, file_info.hash_value)  # Query the TSD table to get the row_id
        if row_id != '0':
            # check before the insert such that the Auto-incr does not incr the rows count
            # Duplicate file - the hash value exists in the tsd_table
            status.add_error("Failed to process JSON file: '%s' - row ID %s with the same hash in tsd_info" % (file_info.file_name, row_id))
            was_renamed = False
            new_name = file_info.file_name
            ret_val = process_status.Duplicate_JSON_File
        else:
            tsd_member = member_id      # The member ID of this node
            ret_val = process_status.SUCCESS

    if not ret_val:

        row_id, file_time = db_info.tsd_insert_entry(status, tsd_member, file_info)
        if row_id == '0':
            # Duplicate file - the hash value exists in the tsd_table
            if not file_info.tsd_member:
                table_name_prefix = str(tsd_member)
            else:
                table_name_prefix = str(file_info.tsd_member)
            status.add_error("Failed to process JSON file: '%s' - duplicate JSON file processed in tsd_%s" % (file_info.file_name, table_name_prefix))
            was_renamed = False
            new_name = file_info.file_name
            ret_val = process_status.Duplicate_JSON_File
        else:

            if not file_info.tsd_member:
                # File provided by a device
                file_info.tsd_member = member_id      # Current node ID in the cluster
                file_info.tsd_row_id = row_id
                file_info.tsd_date = file_time

            was_renamed, new_name = file_info.make_json_file(status)   # set new file name

            ret_val = process_status.SUCCESS

    return [ret_val, was_renamed, new_name, row_id]

# ----------------------------------------------------------
# Process JSON File
# ----------------------------------------------------------
def process_json_file(status, config, file_info, member_id):

    # tsd_name + tsd_id are entered to the data row

    if not file_info.tsd_member:
        tsd_name = "0"              # No TSD used
    else:
        tsd_name = str(file_info.tsd_member)
    tsd_id = file_info.tsd_row_id
    json_file = file_info.get_file_name()

    sql_file_list, rows_count = map_json_to_insert.map_json_file_to_insert(status, tsd_name, tsd_id, file_info.dbms_name, file_info.table_name, 1, json_file, config.watch_dir, file_info.instructions)
    if sql_file_list and len(sql_file_list):
        if config.is_distributor and not file_info.is_from_cluster_member(member_id):
            # This file is from a device and is moved to a distributor
            ret_val = utils_io.manipulate_file(status, json_file, config.json_is_compress, config.json_is_move, config.json_is_delete, config.distr_dir, None, False)
        elif config.is_archive:
            # This file is from a cluster member and is moved to archive
            ret_val = utils_io.archive_file(status, "json", config.archive_dir, config.err_dir, json_file, False)
        else:
            # if the file is moved to destination directory --> RENAME the file (using the unqiue_key) to include the row_id and file_time
            # Always delete so he file is not updated recursively
            ret_val = utils_io.manipulate_file(status, json_file, config.json_is_compress, config.json_is_move, True, config.bkup_dir, None, True)
    else:
        ret_val = process_status.ERR_json_to_insert

    return [ret_val, sql_file_list, rows_count]

# ----------------------------------------------------------
# Move a file that was processed in the streaming data to the distributor or archive
# This file was processed with the flag write_immediate. The streaming process
# Updated the local tables and the file is moved to the distributor or archive
# Details are here - https://anylog.atlassian.net/wiki/spaces/ND/pages/1465843713/Adding+Data+to+a+local+database
# ----------------------------------------------------------
def move_processed_json_file(status, config, file_info, tsd_name, json_file):

    updated_name = json_file.replace("@", str(tsd_name))        # Set the Cluster Member ID of this node on the file name
    if not utils_io.rename_file(status, json_file, updated_name):
        status.add_error("Failed to rename file: %s" % json_file)
        ret_val = process_status.File_move_failed
    else:
        if config.is_distributor:
            # Move to distributor
            ret_val = utils_io.manipulate_file(status, updated_name, config.json_is_compress, config.json_is_move,
                                               config.json_is_delete, config.distr_dir, None, False)
        else:
            # move to archive
            ret_val = utils_io.archive_file(status, "json", config.archive_dir, config.err_dir, updated_name, False)

    return ret_val

# ----------------------------------------------------------
# Process SQL File - load to a dbms
# ----------------------------------------------------------
def process_sql_file(status, config, dbms_name, table_name, file_name):

    ret_val, rows_counter = db_info.process_sql_from_file(status, dbms_name, table_name, file_name)
    if ret_val:
        ret_code = utils_io.manipulate_file(status, file_name, config.sql_is_compress, config.sql_is_move, True, config.bkup_dir, None, True)
        if not ret_code:
            ret_val = True
        else:
            ret_val = False
    else:
        status.add_error("Failed to process SQL from file: " + file_name)

    return [ret_val, rows_counter]


# -----------------------------------------------------------------
# Update statistics on files processed
# -----------------------------------------------------------------
def update_stats(meta_info, table_key, write_immediate, tsd_info_updated):
    '''
    meta_info - the statistics info on the JSON or SQL updates
    table_key - dbms_name.table_name
    write_immediate - True means every entry was updated when arrived (no need to update the current dbms)
    tsd_info_updated - True when data is from sensors (vd from servers supporting the cluster)
    '''
    global  last_file_time_
    if not table_key in meta_info.keys():
        meta_info[table_key] = [0,0,0,0]
        # The entries as a f(table):
        # 1) Counter to the number of json files processed
        # 2) Counter to the number of json files from streaming with write_immediate flag
        # 3) Date and time for the last file processed
        # 4) Date and time for the last file processed - if the data is comming from a device (tsd_info) is updated

    if write_immediate:
        meta_info[table_key][1] += 1  # count files updated in the streaming process
    else:
        meta_info[table_key][0] += 1  # count files updated by the operator

    current_time = utils_columns.get_current_time_in_sec()
    meta_info[table_key][2] = current_time
    if tsd_info_updated:
        meta_info[table_key][3] = current_time

    last_file_time_ = current_time

# -----------------------------------------------------------------
# Get info on the ingestion from sources which are not from other nodes in the cluster
# Satisfy the command: get local ingestion
# Get the date and time of the last update on this node - it is used to
# select a node to process the query (when multiple nodes support the same cluster)
# -----------------------------------------------------------------
def get_local_ingestion(status, io_buff_in, cmd_words, trace):

    global meta_info_json_


    table_sync_time = get_table_sync_time()
    current_time = utils_columns.get_current_time_in_sec()
    reply_table = []

    for key, update_time in table_sync_time.items():

        time_diff = current_time - update_time       # Calculate the time diff to the last insert to this table
        hours_time, minutes_time, seconds_time = utils_data.seconds_to_hms(time_diff)
        elapsed_time = "%02u:%02u:%02u" % (hours_time, minutes_time, seconds_time)
        reply_table.append((key, elapsed_time))



    reply = utils_print.output_nested_lists(reply_table, "",
                                                        ["DBMS.Table", "Elapsed Time"], True, "")

    return [process_status.SUCCESS, reply, "table"]

# -----------------------------------------------------------------
# Get the date and time in which every table is in sync.
# The HA process is using this query to sync the different nodes in the cluster
# such that queries show the same result with different nodes (avoiding race conditions in the sync).
# -----------------------------------------------------------------
def get_table_sync_time():
    global meta_info_json_

    reply_json = {}

    if meta_info_json_:
        for key, value in meta_info_json_.items():
            update_time = value[3]
            if update_time:
                reply_json[key] = update_time

    return reply_json
# -----------------------------------------------------------------
# Show the operator configuration
# -----------------------------------------------------------------
def show_info(status, query_type, format):

    if query_type == "stat":
        info_str = get_stat()
    elif query_type == "summary":
        if format == "json":
            info_str = output_summary_json(status)
        else:
            info_str = output_summary(status)
    else:
        if format == "json":
            info_str = output_json(status)
        else:
            info_str = output_info(status)

    return info_str

# -----------------------------------------------------------------
# Show summary info on the operator
# Command: get operator summary format = json
# -----------------------------------------------------------------
def output_summary_json(status):

    global error_info_
    global is_running
    global statistics_

    summary_dict = {}

    if is_running:
        current_status = "Active"
        current_time = utils_columns.get_current_time_in_sec()
        hours_time, minutes_time, seconds_time = utils_data.seconds_to_hms(current_time - start_time)
        operational_time = "%02u:%02u:%02u" % (hours_time, minutes_time, seconds_time)
        total_rows = statistics_["Total events"]
        delta_rows = statistics_["Delta events"]        # from previous call

        errors_counter =  error_info_[0][1]     # Duplicate JSON files
        errors_counter += error_info_[1][1]     # Counter of the number of JSON files failed to be processed
        errors_counter += error_info_[2][1]     # Error SQL files

    else:
        current_status = "Not Active"
        operational_time = "00:00:00"
        total_rows = 0
        delta_rows = 0
        errors_counter = 0


    summary_dict["Status"] = current_status
    summary_dict["Operational"] = operational_time
    summary_dict["Total Rows"] = total_rows
    summary_dict["Delta Rows"] = delta_rows
    summary_dict["Errors"] = errors_counter

    info_str = utils_json.to_string(summary_dict)

    statistics_["Delta events"] = 0

    return info_str

# -----------------------------------------------------------------
# Show summary info on the operator
# Command: get operator summary
# -----------------------------------------------------------------
def output_summary(status):

    global error_info_
    global is_running
    global statistics_

    summary_list = []

    if is_running:
        current_status = "Active"
        current_time = utils_columns.get_current_time_in_sec()
        hours_time, minutes_time, seconds_time = utils_data.seconds_to_hms(current_time - start_time)
        operational_time = "%02u:%02u:%02u" % (hours_time, minutes_time, seconds_time)
        total_rows = format(statistics_["Total events"], ",")
        delta_rows = format(statistics_["Delta events"], ",")         # from previous call

        errors_counter =  error_info_[0][1]     # Duplicate JSON files
        errors_counter += error_info_[1][1]     # Counter of the number of JSON files failed to be processed
        errors_counter += error_info_[2][1]     # Error SQL files
        errors_counter = format(errors_counter, ",")

    else:
        current_status = "Not Active"
        operational_time = "00:00:00"
        total_rows = 0
        delta_rows = 0
        errors_counter = 0

    summary_list.append((current_status, operational_time, total_rows, delta_rows, errors_counter))

    info_str = utils_print.output_nested_lists(summary_list, "", ["Status", "Operational", "Total Rows", "Delta Rows", "Errors"], True)

    statistics_["Delta events"] = 0

    return info_str


# -----------------------------------------------------------------
# Show info about the files transferred in json format
# -----------------------------------------------------------------
def output_json(status):

    global error_info_
    global meta_info_json_
    global meta_info_sql_

    current_status = {}
    member_id = metadata.get_node_cluster_id()
    if member_id:
        current_status["Member"] = member_id
        current_status["Policy"] = metadata.get_node_policy_id()
        current_status["Cluster"] = metadata.get_node_cluster_id()
    else:
        current_status["Member"] = " Not a member"

    if is_running:
        current_status["Status"] = "Active"

        current_time = utils_columns.get_current_time_in_sec()
        hours_time, minutes_time, seconds_time = utils_data.seconds_to_hms(current_time - start_time)
        current_status["Time"] = "%u:%u:%u (H:M:S)" % (hours_time, minutes_time, seconds_time)

        meta_info = meta_info_json_
        files_type = "JSON processed"
        for i in range(2):      # Output the JSON + SQL file processes
            if len(meta_info):

                if files_type not in current_status:
                    current_status[files_type] = {}

                for key, value in meta_info.items():
                    index = key.find('.')
                    dbms_name = key[:index]
                    if dbms_name not in current_status[files_type]:
                        current_status[files_type][dbms_name] = {}
                    table_name = key[index + 1:]
                    if table_name not in current_status[files_type][dbms_name]:
                        current_status[files_type][dbms_name][table_name] = {}

                    current_status[files_type][dbms_name][table_name]["Files"] = value[0]
                    current_status[files_type][dbms_name][table_name]["Immediate"] = value[1]
                    current_status[files_type][dbms_name][table_name]["Time"] = value[2]

            meta_info = meta_info_sql_
            files_type = "SQL Processed"

        current_status["Duplicate JSON files"] =  error_info_[0][1]
        current_status["Error JSON files"] = error_info_[1][1] # Counter of the number of JSON files failed to be processed
        current_status["Error SQL files"] = error_info_[2][1]

    else:
        current_status["Status"] = "Not Active"

    info_str = utils_json.to_string(current_status)
    return info_str

# -----------------------------------------------------------------
# Reset the timers and statistics - reset operator
# -----------------------------------------------------------------
def reset_stat(status, io_buff_in, cmd_words, trace):
    global first_file_time_
    global last_file_time_
    global meta_info_json_
    global meta_info_sql_

    first_file_time_ = 0
    last_file_time_ = 0
    meta_info = meta_info_json_
    for i in range(2):
        if meta_info:
            for table_info in meta_info.values():
                table_info[0] = 0   # Reset the number of files processed
                table_info[1] = 0  # Reset the number of write_immediate files processed
                table_info[2] = 0  # Date and time for the last file processed

        meta_info = meta_info_sql_
    return process_status.SUCCESS
# -----------------------------------------------------------------
# Show info about the files transferred
# -----------------------------------------------------------------
def output_info(status):

    global meta_info_json_
    global meta_info_sql_
    global  error_info_
    global current_config
    global start_time

    # Show stat on the JSON files and the SQL files

    member_cmd.blockchain_load(status, ["blockchain", "get", "cluster"], False, 0)    # Load updated copy of the metadata

    member_id = metadata.get_node_member_id()  # The ID show operator of this node in the cluster

    if is_running:
        current_time = utils_columns.get_current_time_in_sec()
        hours_time, minutes_time, seconds_time = utils_data.seconds_to_hms(current_time-start_time)
        info_str =  "\r\nStatus:     Active"
        info_str += "\r\nRun Time:   %02u:%02u:%02u (H:M:S)" % (hours_time, minutes_time, seconds_time )
        # load time - from the first file loaded to the last loaded
        time_diff = last_file_time_ - first_file_time_
        if time_diff < 0:
            time_diff = 0       # because reset may be done while threads are operating (using blockchain reset command)
        hours_time, minutes_time, seconds_time = utils_data.seconds_to_hms(time_diff)
        info_str += "\r\nLoad Time:  %02u:%02u:%02u (H:M:S)" % (hours_time, minutes_time, seconds_time)
    else:
        info_str =  "\r\nStatus:     Not Active"

    if member_id:
        policy_id = metadata.get_node_policy_id()  # A cluster ID associated with this node
        info_str += "\r\nPolicy:     %s" % policy_id
        cluster_id = metadata.get_node_cluster_id()  # A cluster ID associated with this node
        info_str += "\r\nCluster:    %s" % cluster_id
        info_str += "\r\nMember:     %s" % str(member_id)
    else:
        info_str += "\r\nCluster:    Not a member"

    if is_running:
        meta_info = meta_info_json_
        files_type = "JSON"
        for i in range(2):

            if len(meta_info):

                output_list = []
                for key, value in meta_info.items():
                    index = key.find('.')
                    dbms_name =  key[:index]
                    table_name = key[index + 1:]
                    files_counter = value[0]
                    immediate_counter = value[1]
                    time_diff = utils_columns.get_current_time_in_sec() - value[2]
                    hours_time, minutes_time, seconds_time = utils_data.seconds_to_hms(time_diff)
                    elapsed_time = "%02u:%02u:%02u" % (hours_time, minutes_time, seconds_time)
                    output_list.append((dbms_name, table_name, files_counter, immediate_counter, elapsed_time))

                info_str += utils_print.output_nested_lists(output_list, f"Statistics {files_type} files", ["DBMS", "Table", "Files","Immediate", "Elapsed Time"], True)
            meta_info = meta_info_sql_
            files_type = "SQL"


            # A list with error type + counter, last error code + last error message

        for i in range (len(error_info_)):
            if error_info_[i][1]:
                if not i:
                    # The error showing duplicate JSON files is monitored al location 0 of the list
                    error_info_[i][4] = process_status.Duplicate_JSON_File
                    error_info_[i][5] = "Duplicate JSON files"
                else:
                    # error in processing JSON/SQL file
                    last_error = error_info_[i][4]
                    if last_error:
                        message = process_status.get_status_text(last_error)
                    else:
                        message = ""
                    error_info_[i][5] = message


        info_str += utils_print.output_nested_lists(error_info_, "Errors summary", ["Error Type", "Counter", "DBMS Name","Table Name", "Last Error", "Last Error Text"], True, "")

    else:
        info_str += "\r\nStatistics: Not Available"

    return info_str

# ------------------------------------------------------------------------------
# If the table is not assigned to an operator or a cluster
# Associate a table to the operator in one of 2 methods:
# 1. Assign the table to the operator
# Or
# 2.  Assign the table to a cluster
# ------------------------------------------------------------------------------
def assign_table(status, cluster_id, config, dbms_name, table_name, trace_level):

    # The IP and port of the operator
    ip_port_string = net_utils.get_external_ip_port()
    if not ip_port_string:
        status.add_error("The Operator is not able to identify the local TCP IP and Port")
        ret_val = process_status.ERR_process_failure
    else:

        ip_port = ip_port_string.split(":")
        if len(ip_port) != 2:
            status.add_error("The Operator is not able to identify the local TCP IP and Port")
            ret_val = process_status.ERR_process_failure
        else:
            ret_val = process_status.SUCCESS
            # Is the table declared in the metadata
            table_supported = metadata.is_table_supported(status, config.company_name, dbms_name, table_name )

            if not table_supported:  # This Operator, or this cluster, is not associated with the table
                # associate the table to an operator or a cluster
                if config.is_create_table:
                    ret_val = add_table_owner(status, cluster_id, config, ip_port[0], ip_port[1], config.company_name, dbms_name, table_name, trace_level)
                else:
                    status.add_error("Operator 'create_table' flag is set to 'false' with table: '%s.%s' not assigned" % (dbms_name, table_name))
                    ret_val = process_status.Operator_not_allowed_with_table


    return ret_val
# ------------------------------------------------------------------------------
# Return an info string on the Operator state
# ------------------------------------------------------------------------------
def get_info(status):
    global is_running
    global status_queue_
    global current_config

    get_metadata_info(status)  # This call will set the correct message in the status_queue when the user calls: "show processes"

    if is_running:
        ip_port = interpreter.get_one_value(current_config, "master_node")
        if not ip_port:
            master_node = "False"
        else:
            master_node = ip_port

        info_str = status_queue_.get_indexed_msg([("{A1}",master_node)])
    else:
        info_str = ""
    return info_str

# ------------------------------------------------------------------------------
# Associate the table to an Operator or to a cluster
# ------------------------------------------------------------------------------
def add_table_owner(status, metadata_cluster_id, config, ip, port, company_name, dbms_name, table_name, trace_level):

    global cmd_get_operator

    if metadata_cluster_id == '0':
        cluster_id = '0'
        cmd_get_operator[6] = ip
        cmd_get_operator[10] = port
        # there is no metadata layer defined - test if the operator is associated with a cluster
        ret_val, operators_list = member_cmd.blockchain_get(status, cmd_get_operator, config.blockchain_file, True)
        if not ret_val and len(operators_list):
            # take info from from first operator
            if "cluster" in operators_list[0]["operator"]:
                cluster_id = operators_list[0]["operator"]["cluster"]
                if "company" in operators_list[0]["operator"]:
                    company_by_cluster = operators_list[0]["operator"]["company"]
                else:
                    company_by_cluster = ""
    else:
        ret_val = process_status.SUCCESS
        # get the info for the cluster policy from the metadata layer
        cluster_id = metadata_cluster_id
        company_by_cluster = metadata.get_company_name()

    if not ret_val:
        if trace_level:
            if cluster_id == '0':
                policy_type = "Operator"
            else:
                policy_type = "Cluster"
            message = "[Operator] [Assign policy type '%s' to table] [%s: %s.%s]" % (policy_type, company_name, dbms_name, table_name)
            utils_print.output(message, True)


        if cluster_id != '0':
            if metadata.is_table_in_cluster(status, company_by_cluster, dbms_name, table_name, cluster_id):
                # This node is processing this table's data
                return process_status.SUCCESS

            # Get the cluster name from the local blockchain
            cluster = {}
            cluster["parent"] = cluster_id
            cluster["name"] = metadata.get_cluster_name()
            cluster["company"] = company_by_cluster
            cluster["table"] = [
                {
                    "dbms" : dbms_name,
                    "name" : table_name
                 }
            ]
            cluster["source"] = "Node at %s:%s" % (ip, port)
            policy = {"cluster": cluster}  # The JSON table to update the blockchain
        else:
            # Return an error as the cluster ID was not found
            ret_val = process_status.No_cluster_assigned    # no cluster assigned to the operator

        if not ret_val:
            if config.platform == "master":
                platform = None     # not using a blockchain
            else:
                platform = [config.platform]
            ret_val = member_cmd.blockchain_insert_all(status, mem_view, policy, True, config.blockchain_file, [config.master_node], platform)

    return ret_val

# ------------------------------------------------------------------------------
# Statistics to monitor performance of the node
# ------------------------------------------------------------------------------
def stat_reset():
    global statistics_

    statistics_ = {
        "Node name" :   "",
        "Status" : "Active",
        "Start timestamp": utils_columns.get_current_time_in_sec(),   # The date and time operator started
        "Query timestamp": 0,  # The timestamp of previous query
        "Operational time": "",      # HH:MM:SS of operations
        "Events/second": 0,     # Insert/second since last call
        "Total events": 0,      # Since started
        "Delta events": 0,        # Since last call
        "Delta time": "",       # Time from last call for stat
    }
# ------------------------------------------------------------------------------
# Statistics on new events - Update with events successfully processed
# ------------------------------------------------------------------------------
def stat_new_events( counter ):
    global statistics_

    statistics_["Total events"] += counter
    statistics_["Delta events"] += counter      # Events processed since last query

# ------------------------------------------------------------------------------
# Return Statistics, calculate events\second and reset delta
# ------------------------------------------------------------------------------
def get_stat():

    global statistics_
    global is_running

    utils_monitor.update_process_statistics(statistics_, True, is_running)

    info_str = utils_json.to_string(statistics_)

    return info_str

# ------------------------------------------------------------------
# Return info on the workers pool
# returns info when calling - get operator pool
# ------------------------------------------------------------------
def get_threads_obj():

    global operator_pool_
    return operator_pool_
