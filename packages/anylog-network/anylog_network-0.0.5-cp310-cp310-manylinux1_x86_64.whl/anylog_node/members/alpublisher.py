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
import anylog_node.blockchain.blockchain as blockchain
import anylog_node.generic.params as params
import anylog_node.json_to_sql.suggest_create_table as suggest_create_table
import anylog_node.generic.utils_io as utils_io
import anylog_node.generic.utils_data as utils_data
import anylog_node.generic.utils_columns as utils_columns
import anylog_node.generic.utils_print as utils_print
import anylog_node.tcpip.message_header as message_header
import anylog_node.blockchain.al_auth as al_auth
import anylog_node.blockchain.bsync as bsync
import anylog_node.blockchain.metadata as metadata

mem_view = None
is_running = False
on_wait = False  # waiting for blockchain
cmd_get_table = ["blockchain", "get", "table", "where", "dbms", "=", "dbms", "and", "name", "=", "table"]
cmd_create = ["run", "client", "(operators)", "sql", None, "text", None]
table_info = {"table": {} }
cmd_get_distribution = None
blockchain_push = ["run", "client", None, "blockchain", "push", "json"]

tables_dest = {}  # A dictionary that shows for ech table, a destination server (updated using distribution policies)

meta_info = {}  # A dictionary with info on the tables processed

file_to_error = 0  # counter of files moved to err dir

current_config = None  # A ptr to the configuration values so it can e printed


# The distribution info is a dictionary as f(dbms + table) pointing to a list with info: a) ID of next b) List of dest c) Counter files tranferred
distribution_info = {}       # A dictionary of distributions based on user definitions

# ----------------------------------------------------------
# Process of a publisher
# run publisher where company = anylog and delete_json = False and delete_sql = False
# ----------------------------------------------------------
def run_publisher(dummy: str, conditions: dict):
    global mem_view
    global is_running
    global on_wait
    global file_to_error
    global cmd_get_distribution
    global current_config
    global distribution_info  # A dictionary of distributions based on user definitions

    process_status.reset_exit("publisher")

    current_config = conditions

    status = process_status.ProcessStat()

    node_id = al_auth.get_node_id(status)
    if not node_id:
        # Publisher ignores policies that direct the current node to distribute the data to specific operators
        process_log.add_and_print("event", "Missing node ID - publisher ignores Distribution Policies")
    else:
        cmd_get_distribution = ["blockchain", "get", "distribution", "where", "publisher", "=", node_id]

    watch_dir = interpreter.get_one_value(conditions, "watch_dir")
    err_dir = interpreter.get_one_value(conditions, "err_dir")
    bkup_dir = interpreter.get_one_value(conditions, "bkup_dir")
    file_types = conditions["file_type"]  # get the list of file types to consider

    file_sections = [0, 1, 2, 3, 4, 5]  # [dbms name].[table name].[data source].[hash value].[instructions].[TSD name].[TSD ID].[TSD date]

    company_name = interpreter.get_one_value(conditions, "company")
    if not company_name or company_name == '*':
        # This is the case that company name is the same as the database name
        any_company = True
    else:
        any_company = False

    is_compress = interpreter.get_one_value(conditions, "compress_json")
    is_move = interpreter.get_one_value(conditions, "move_json")
    is_delete = interpreter.get_one_value(conditions, "delete_json")

    master_node = interpreter.get_one_value(conditions, "master_node")

    blockchain_file = interpreter.get_one_value(conditions, "blockchain_file")
    on_wait = True
    ret_val = blockchain.wait_for_blockchain(status, blockchain_file, 30)
    on_wait = False
    if ret_val:
        process_log.add_and_print("event", "Publisher process terminated: No local blockchain data")
        is_running = False
        current_config = None
        return

    get_distribution_policies(status, blockchain_file)

    is_running = True

    if not mem_view:
        data_buffer = bytearray(params.TCP_BUFFER_SIZE)
        mem_view = memoryview(data_buffer)  # not using one instance as it may be overwritten before message send

    operators = None

    while 1:

        file_list = []  # needs to be inside the while loop to be initiated (as the same file will be called again)

        ret_val, file_name = member_cmd.get_files_from_dir(status, "publisher", 5, watch_dir, "file", file_types,
                                                           file_list, None, None, False)

        trace_level = member_cmd.commands["run publisher"]['trace']

        if ret_val:
            # Including Publisher terminated - or global termination
            break
        else:
            process_file = True
            process_completed = False
            # get the table name and the database name from the file name
            dbms_name, table_name, source, hash_value, instructions, tsd_member, tsd_row_id, tsd_date = utils_io.query_file_name(file_name, file_sections)

            if not dbms_name or not table_name:
                status.add_error("Publisher failed to retrieve dbms name and table name from file: '%s'" % file_name)
                process_file = False
            else:
                if any_company:
                    # use the dbms_name as the company name
                    company_name = metadata.get_company_by_dbms(dbms_name)    # the metadata maintains companies as f(dbms_name)
                    if not company_name:
                        company_name = dbms_name                            # Assume the dbms name is the company name

                table_key = dbms_name + '.' + table_name
                if trace_level > 1:
                    utils_print.output("[Publisher] [New File] [" + table_key + "]", True)

                # test if the dbms and table are in the limit_table list
                if "limit_tables" in conditions.keys():
                    # only listed tables are allowed
                    if table_key not in conditions["limit_tables"]:
                        status.add_error(
                            "Publisher process: Retrieved a file which fails to satisfy 'limit_tables': '%s'" % file_name)
                        process_file = False

            if process_file:

                if table_key in distribution_info:
                    operators = get_operator_from_config(table_key)     # If user provided a definition
                elif dbms_name + '.*' in distribution_info:
                    operators = get_operator_from_config(dbms_name + '.*')  # If user provided a definition
                elif '*.*' in distribution_info:
                    operators = get_operator_from_config('*.*')  # If user provided a definition
                else:
                    ret_val, operators = get_dest_operators(status, company_name, dbms_name, table_name, blockchain_file)
                    if ret_val:
                        process_file = False

                if trace_level > 1:
                    utils_print.output("[Publisher] [Use Operators] [" + operators + "]", True)

            if process_file:
                # create a dictionary that maintains info on each table processed
                # Each entry is an array.
                # The first entry in the array is the Operator ID to use
                if not table_key in meta_info.keys():
                    meta_info[table_key] = []
                    meta_info[table_key].append(0)  # use operator # 0
                    meta_info[table_key].append(0)  # Counter to the number of files send
                    meta_info[table_key].append("")  # Date and time for the last file send
                    meta_info[table_key].append("")  # Destination IP and Port

                if file_name.endswith(".json"):
                    ret_val = create_table(status, blockchain_file, master_node, operators, file_name, dbms_name,
                                           table_name, True, instructions, trace_level)
                    if ret_val:
                        process_file = False  # error in table creation

            if process_file:
                ret_val =  trasfer_file(status, operators, file_name, table_key, trace_level)  # copy a file to a different machine
                if not ret_val:
                    process_completed = True

            if process_completed:
                if trace_level > 1:
                    utils_print.output("[Publisher] [File Transferred]", True)

                ret_val = utils_io.manipulate_file(status, file_name, is_compress, is_move, is_delete, bkup_dir, None, True)
                if ret_val:
                    break
            else:
                # failed to process the file --> move to error
                if trace_level > 1:
                    utils_print.output("[Publisher] [File Transfer Failed]", True)

                file_to_error += 1
                erro_str = "err_%u" % ret_val
                if not utils_io.file_to_dir(status, err_dir, file_name, erro_str, True):
                    break

    process_log.add_and_print("event", "Publisher process terminated: %s" % process_status.get_status_text(ret_val))
    is_running = False
    current_config = None

# -----------------------------------------------------------------
# Get destination operators
# A) If a policy designates specific operators - use this policy
# B) Take Operators from a metadata layer
# C) If no metadata operators - take from the blockchain
# -----------------------------------------------------------------
def get_dest_operators(status, company_name, dbms_name, table_name, blockchain_file):

    operators = get_named_operators(status, dbms_name, table_name)  # Get operators by a policy that names the operators
    if not operators:
        # get info from the blockchain
        ret_val = member_cmd.blockchain_load(status, ["blockchain", "get", "cluster"], False, 0)
        if ret_val == process_status.Needed_policy_not_available:
            ret_val = process_status.SUCCESS

        if not ret_val:

            # version changed
            operators = member_cmd.get_operators_ip_by_table(status, blockchain_file, company_name, dbms_name, table_name)

            if not operators:
                status.add_error("Publisher process: Operators for table '%s.%s' not identified" % (dbms_name, table_name))
                ret_val = process_status.Missing_operators_for_table


    return [ret_val, operators]

# -----------------------------------------------------------------
# copy the file to a different machine
# With multiple operators, determine the Operators to use
# -----------------------------------------------------------------
def trasfer_file(status, operators, file_name, table_key, trace_level):
    global meta_info

    operators_list = operators.split(',')
    counter_operators = len(operators_list)
    if counter_operators == 1:
        receiver = operators  # only one operator
    else:
        id = meta_info[table_key][0]
        if id >= counter_operators:
            id = 0
        meta_info[table_key][0] = id + 1  # set next receiver
        receiver = operators_list[id]

    index = receiver.find(":")
    if index <= 0 or index == (len(receiver) - 1):
        status.add_error(
            "Failed to identify IP and Port using: '%s' of Operator supporting table: '%s'" % (receiver, table_key))
        return process_status.Missing_operators_for_table

    dest_name, dest_type = utils_io.extract_name_type(file_name)
    dest_file_name = dest_name + "." + dest_type

    # copy the file to one or more standbys
    ret_val = member_cmd.transfer_file(status, [(receiver[:index], receiver[index + 1:])], file_name, dest_file_name,
                                       message_header.GENERIC_USE_WATCH_DIR, trace_level, "Publisher", True)

    if not ret_val:
        meta_info[table_key][1] += 1  # number of files send
        meta_info[table_key][2] = utils_columns.get_current_time("%Y-%m-%d %H:%M:%S")
        meta_info[table_key][3] = receiver
    return ret_val
# -----------------------------------------------------------------
# Create new table
# cmd_get_table = ["blockchain", "get", "table", "where", "dbms", "=" "dbms", "and", "table", "=", "table"]
# -----------------------------------------------------------------
def create_table(status, blockchain_file, master_node, operators, file_name, dbms_name, table_name, with_tsd_info, instructions,
                 trace_level):
    global mem_view
    global cmd_get_table
    global cmd_create
    global blockchain_push

    if cmd_get_table[6] != dbms_name:
        cmd_get_table[6] = dbms_name
    if cmd_get_table[10] != table_name:
        cmd_get_table[10] = table_name

    ret_val, existing_table = member_cmd.blockchain_get(status, cmd_get_table, blockchain_file, True)
    if not ret_val and existing_table:
        # Table exists in blockchain
        return process_status.SUCCESS

    if instructions and instructions != '0':
        # test if instructions define how to create the table
        instruct = member_cmd.get_instructions(status, instructions)
    else:
        instruct = None

    create_stmt = suggest_create_table.suggest_create_table(status, file_name, dbms_name, table_name, with_tsd_info, instruct)

    if trace_level > 1:
        utils_print.output("[Publisher] [Create Table from Data] [" + create_stmt + "]", True)

    if not create_stmt:
        return process_status.Failed_to_analyze_json
    create_stmt = utils_data.replace_string_chars(True, create_stmt, {'|': '"'})

    table_info["table"]["name"] = table_name
    table_info["table"]["dbms"] = dbms_name
    table_info["table"]["create"] = create_stmt

    if master_node:
        if trace_level > 1:
            utils_print.output("[Publisher] [Send Table Definition to Master] [" + master_node + "]", True)

        if not blockchain_push[2]:
            blockchain_push[2] = "(" + master_node + ")"
        blockchain_push[5] = str(table_info)
        ret_val = member_cmd.run_client(status, mem_view, blockchain_push, 0)
    else:
        if trace_level > 1:
            utils_print.output("[Publisher] [Update Table Definition on Local Node]", True)

        if not blockchain.blockchain_write(status, blockchain_file, table_info, True):
            ret_val = process_status.ERR_process_failure

    if not ret_val:

        cmd_create[2] = "(%s)" % operators
        cmd_create[4] = dbms_name
        cmd_create[6] = create_stmt
        ret_val = member_cmd.run_client(status, mem_view, cmd_create, 0)
        if ret_val:
            status.add_error("Failed to send CREATE TABLE statement to %s" % operators)

    return ret_val


# -----------------------------------------------------------------
# Get Operators by dbms name and table name
# -----------------------------------------------------------------
def get_named_operators(status, dbms_name, table_name):
    global tables_dest  # a table representing data distribution policy for this Publisher

    if len(tables_dest):
        try:
            # Get operators from the distribution policy
            operators = tables_dest[dbms_name + '.' + table_name]
        except:
            operators = ""

        if not operators:
            try:
                # Get operators from the distribution policy
                operators = tables_dest[dbms_name + '.*']
            except:
                operators = ""

        if not operators:
            try:
                # Get operators from the distribution policy
                operators = tables_dest['*']
            except:
                operators = ""
    else:
        operators = ""

    return operators
# -----------------------------------------------------------------
# Show info about the files transferred
# -----------------------------------------------------------------
def show_info():
    global file_to_error
    global tables_dest
    global current_config

    if current_config:
        info_str = '\r\nConfiguration:\r\n'
        info_str += utils_print.format_dictionary(current_config, True, False, False, ["Key", "Value"]) + "\r\n"
    else:
        info_str = ""

    if len(tables_dest):
        # Print list of destinations
        info_str += '\r\nDestinations:\r\n'
        info_str += utils_print.format_dictionary(tables_dest, True, False, False, ["Table", "Operator"]) + "\r\n"

    if len(meta_info) or file_to_error:
        if len(meta_info):
            info_str += '\r\nStatistics:\r\n' \
                        'DBMS                   TABLE                  FILES      LAST TRANSFER       DESTINATION\r\n' \
                        '---------------------- ---------------------- ---------- ------------------- -------------------\r\n'

            for key, value in meta_info.items():
                index = key.find('.')
                info_str += key[:index].ljust(22)[:22] + ' '
                info_str += key[index + 1:].ljust(22)[:22] + ' '
                info_str += str(value[1]).rjust(10)[:10] + ' '  # Counter files
                info_str += value[2] + ' '      # Date last file transfer
                info_str += value[3] + '\r\n'   # Destination

        info_str += "\r\nFiles moved to error dir: %6u" % file_to_error
    else:
        info_str += " - no statistical data"

    return info_str


# -----------------------------------------------------------------
# Get the Policies (if available) that instruct node how to distribute the data
# -----------------------------------------------------------------
def get_distribution_policies(status, blockchain_file):
    global cmd_get_distribution
    global tables_dest

    if cmd_get_distribution:
        ret_val, distributions = member_cmd.blockchain_get(status, cmd_get_distribution, blockchain_file, True)
        if ret_val:
            # Error getting distributions
            return ret_val
    else:
        # There is no node id - distributions ignored
        distributions = None

    if not distributions or not isinstance(distributions, list):
        # No such policies
        return process_status.SUCCESS

    for distribution in distributions:
        try:
            dist_table = distribution["distribution"]["destinations"]
        except:
            status.add_error("Missing information in Distribution Policy")
        else:
            if isinstance(dist_table, list):
                # A table with destinations for tables
                for destination in dist_table:
                    try:
                        ip_port = destination["ip_port"]
                        tables = destination["tables"]
                    except:
                        status.add_error("Missing or wrong information in Distribution Policy to determine destination")
                    else:
                        for dbms_table in tables:
                            tables_dest[dbms_table.lower()] = ip_port

    return process_status.SUCCESS

# =======================================================================================================================
# Test if user provided the distribution definitions
# =======================================================================================================================
def get_operator_from_config(table_key):
    global distribution_info  # A dictionary of distributions based on user definitions

    table_info = distribution_info[table_key]

    index = table_info[0]      # The id of the distribution
    destination_list = table_info[1]        # The list of the operators
    if index >= len(destination_list):
        index = 0
        table_info[0] = 0

    dest = destination_list[index]

    table_info[2][index] += 1   # count the number of files transferred
    table_info[0] += 1          # set on next operator

    return dest

# =======================================================================================================================
# Declare how operator distributes the data
# Examples:
# set data distribution where dbms = lsl_demo and table = ping_sensor and dest = 10.12.32.148:2048
# set data distribution where dbms = lsl_demo and table = * and dest = 10.12.32.148:2048 and dest = 10.181.231.18:2048
# set data distribution where dbms = * and dest = 10.12.32.148:2048
# set data distribution where dbms = lsl_demo and table = ping_sensor and remove = true
# =======================================================================================================================
def _distribute_data(status, io_buff_in, cmd_words, trace):

    global distribution_info        # A dictionary of distributions based on user definitions
    #                              Must     Add      Is
    #                              exists   Counter  Unique
    keywords = {"dbms": ("str", True, False, True),
                "table": ("str", False, False, True),
                "dest": ("ip.port", False, True, False),  # The operator that will get the data
                "remove": ("bool", False, False, True),  # The operator that will get the data
                }

    ret_val, counter, conditions = interpreter.get_dict_from_words(status, cmd_words, 4, 0, keywords, False)

    if ret_val:
        return ret_val

    if not counter:
        if not "remove" in conditions or interpreter.get_one_value(conditions, "remove") != True:
            status.add_error("Data distribution error: command requires 'dest' value or 'remove = True'")
            return process_status.ERR_command_struct
        else:
            remove = True
    else:
        remove = False
        destinations = conditions["dest"]

    dbms_name = interpreter.get_one_value(conditions, "dbms")

    table_name = interpreter.get_one_value_or_default(conditions, "table", "*")

    dbms_table = dbms_name + '.' + table_name

    if remove:
        # Remove the distribution definition
        if dbms_table in distribution_info:
            del distribution_info[dbms_table]
    else:
                                        # ID         List of          Counter files
                                        # of next    destinations     Transferred
                                        # dest
        distribution_info[dbms_table] = [0,          destinations,  [0] * len(destinations)]  # A dictionary of distributions based on user definitions


    return ret_val

# =======================================================================================================================
# Return the distribution info
# =======================================================================================================================
def get_distribution(status, io_buff_in, cmd_words, trace):

    global distribution_info        # A dictionary of distributions based on user definitions

    out_info = []
    for dms_table, info in distribution_info.items():
        key_list = dms_table.split('.')
        dbms_name = key_list[0]
        table_name = key_list[1]
        destinations = info[1]      # The list of Operators
        files_count = info[2]       # The list of files transferred (an entry per operator)
        for x in range (len(destinations)):
            out_info.append((dbms_name, table_name, destinations[x], files_count[x]))
            dbms_name = ""
            table_name = ""

    title = ["DBMS", "Table", "Destinations", "Files"]

    output_txt = utils_print.output_nested_lists(out_info, "", title, True)

    return [process_status.SUCCESS, output_txt]

