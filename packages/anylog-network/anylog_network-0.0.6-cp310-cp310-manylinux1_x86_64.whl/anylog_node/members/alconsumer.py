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

import time

import anylog_node.generic.process_status as process_status
import anylog_node.generic.process_log as process_log
import anylog_node.generic.interpreter as interpreter
import anylog_node.dbms.db_info as db_info
import anylog_node.cmd.member_cmd as member_cmd
import anylog_node.blockchain.metadata as metadata
import anylog_node.generic.params as params
import anylog_node.tcpip.message_header as message_header
import anylog_node.generic.utils_print as utils_print

# ------------------------------------------------------------------------------------
# Determines which Source Files are missing on the current node and requests the files
# ------------------------------------------------------------------------------------
consumer_running_flag = False
max_tsd_rows_ = 100            # A limit on the number of tsd_rows that are retrieved to be evaluated
import anylog_node.generic.utils_queue as utils_queue

mem_view_ = None
process_mode_ = "Not enabled"        # 'suspend' - files are not requested

# This is a message to get the info from the cluster members on the TSD status
info_tsd_msg = "run client ip:port event get_recent_tsd_info tsd_id date_start date_end".split(' ')

counter_operators_ = 0  # The number of operators on the same cluster (not including this operator)
active_peers_ = 0       # The number of operators managing this cluster that are active

status_queue_ = utils_queue.MsgQueue(0)

status_info  = [
    "Metadata info not available",
    "No peer Operators supporting the cluster",
    "Registered peers: {1}, Active peers: {2}, Mode: {3}",
]
status_queue_.set_static_queue(status_info)

# ------------------------------------------------------------------------------
# Test if the data synchronizer is running
# ------------------------------------------------------------------------------
def is_consumer_running():
    return consumer_running_flag
# ------------------------------------------------------------------------------
# Return an info string on the consumer state
# ------------------------------------------------------------------------------
def get_info(status):
    global consumer_running_flag
    global counter_operators_
    global status_queue_
    global process_mode_

    if consumer_running_flag:
        info_str = status_queue_.get_indexed_msg( [("{1}", str(counter_operators_)), ("{2}", str(active_peers_)), ("{3}", process_mode_)] )
    else:
        info_str = ""
    return info_str
# ------------------------------------------------------------------------------
# Change the consumer mode
# "active" - request data from peer operator
# and "suspend" - do not request data from peer
# ------------------------------------------------------------------------------
def set_mode(new_mode):
    global process_mode_

    process_mode_ = new_mode
# ------------------------------------------------------------------------------
# Main process:
# run data consumer where start_date = -30d
# run data consumer where start_date = -30d and mode = suspend     # only ask for status
# ------------------------------------------------------------------------------
def data_consumer(dummy: str, conditions: dict):
    global consumer_running_flag
    global mem_view_
    global counter_operators_
    global status_queue_
    global process_mode_

    process_status.reset_exit("consumer")

    status = process_status.ProcessStat()

    ret_val = process_status.SUCCESS

    start_date = interpreter.get_one_value(conditions, "start_date")        # the start time for validation
    end_date = interpreter.get_one_value(conditions, "end_date")            # the end time for validation or if missing - to current time

    process_mode_ = interpreter.get_one_value_or_default(conditions, "mode", "active")  # can be set to suspended

    cmd_load = ["blockchain", "get", "cluster"]

    consumer_running_flag = True


    if not mem_view_:
        data_buffer = bytearray(params.TCP_BUFFER_SIZE)
        mem_view_ = memoryview(data_buffer)  # not using one instance as it may be overwritten before message send

    metadata_version = 0

    while 1:

        if process_status.is_exit("consumer"):
            break

        node_member_id = metadata.get_node_member_id()
        if node_member_id:
            # Only if metadata shows this node is a member of  cluster
            trace_level = member_cmd.commands["run data consumer"]['trace']

            # 1) Updates the metadata tier if the blockchain data was modified
            ret_val = member_cmd.blockchain_load(status, cmd_load, False, 0)
            if ret_val:
                status_queue_.set_index(0)      # Message - "Metadata info not available"
            else:
                # 2) Get the list of destination operators
                if not metadata.test_metadata_version(metadata_version):
                    # if the metadata version was changed, update the metadata
                    operators = metadata.get_operators_info(status, None, False, ["member", "ip", "port"])  # Get the IP + Ports excluding this Operator
                    counter_operators_ = len(operators)  # The number of operators on the same cluster (without the current)
                    if counter_operators_:  # If no operators - No second operator on the cluster
                        # Make sure all TSD tables are represented on the local database
                        create_tsd_tables(status, node_member_id, operators)          # Create tds tables for new operators
                    metadata_version = metadata.get_metadata_version()

                if counter_operators_:
                    status_queue_.set_index(2)  # Message: "X Operators supporting the cluster"
                    # 3) Request an update from the member nodes on the last status of the TSD table
                    ret_val = event_request_tsd_update(status, mem_view_, operators, start_date, end_date)
                    if ret_val:
                        break

                    # 4) For each operator, determine the missing files
                    ret_val = get_missing_files(status, operators, start_date, end_date, trace_level)
                    if ret_val:
                        break
                else:
                    status_queue_.set_index(1)      # Message:  "No peer Operators supporting the cluster"

        process_status.sleep_test_signal(60, "consumer")

    process_log.add_and_print("event", "HA Consumer process terminated: %s" % process_status.get_status_text(ret_val))

    consumer_running_flag = False

# ------------------------------------------------------------------------------
# For each operator, go over the TSD table to determine the missing file
# 1) Query the first TSD ID before the start date
# 2) with end date: Query the first TSD ID after the end date
# 3) Run a count to see if rows are missing
# 4) If Rows are missing - repeat a process to determine missing rows for every 1000 entries
# ------------------------------------------------------------------------------
def get_missing_files(status, operators_list, start_date, end_date, trace_level):

    ret_val = process_status.SUCCESS

    for operator in operators_list:

        member_id = operator[0]
        table_name = "tsd_%s" % str(member_id)

        member_stat = metadata.get_member_stat(table_name)   # maintain the status of files transferred from the member

        if trace_level:
            if not member_stat or member_stat["validated_id"] == '0':
                utils_print.output("\r\n[Consumer] [Sync with: %s] [No Stat Data]" % table_name, True)

        # validated_id - initialized by the source node - The ID which is with a date earlier than the start date (ie -30d: the last ID 30 days ago)
        if member_stat and member_stat["validated_id"] != '0':
            # The source TSD table is with data
            start_id = member_stat["validated_id"]      # The ID to which all previous IDS are complete

            end_id = member_stat["src_last_id"]         # The last ID reported on the source node


            if start_id < end_id:       # if equal --> the last ID is validated
                # Get the number of rows between the start_id and the end_id
                # Done by a query to the TSD table - "select count(*) from tsd_x where file_id >= start_id and file_id <= end_id"
                ret_val, diff = query_difference(status, table_name, start_id + 1, end_id) # start from the next row after the validated row
                if ret_val:
                    break

                if diff:        # changed from if diff != (end_id - start_id):
                    if trace_level:
                        utils_print.output("\r\n[Consumer] [Sync with: %s] [Files missing: %u] [Validated ID: %s] [End ID: %s]" % (table_name, diff, start_id, end_id), True)

                    # retrieves the rows between start_id and end_id and find which is missing - start from the next row after the validated row
                    # And return the first row ID (first_row) that is missing
                    ret_val, first_row = request_missing_files(status,table_name, start_id +1, end_id + 1, operator[1], operator[2], trace_level )
                    if ret_val:
                        continue
                    if first_row:
                        validated_id = first_row - 1    # first_row is the first row ID missing, therefore, the one before is validated
                    else:
                        # There is no difference because the files were received between the calls: [query_difference()] [files received] [request_missing_files()]
                        validated_id = end_id
                else:
                    validated_id = end_id

                member_stat["validated_id"] = validated_id        # All IDS up to end_id exists on the current node
                member_stat["validated_date"] = member_stat["message_time"]  # Use the message time as an indicator of the ID
            else:
                if trace_level > 1:
                    utils_print.output("\r\n[Consumer] [No files missing from member %s] [Validated ID: %s]" % (table_name, start_id), True)
        else:
            if trace_level:
                if not member_stat:
                    utils_print.output("\r\n[Consumer] [member of %s is not represented in the metadata]" % (table_name), True)
                else:
                    utils_print.output("\r\n[Consumer] [Sync with: %s] [No missing files] [Validated ID is 0]" % (table_name), True)


    return ret_val

# ------------------------------------------------------------------------------
# Query TDS info to get a single file_id before or after a specific timestamp
# ------------------------------------------------------------------------------
def query_tsd_entry(status, table_name, query_date, condition)   :

    if condition[0] == "<":
        order = "desc"
    else:
        order = "asc"
    sql_stmt = "select file_id from %s where file_time %s '%s' order by file_time %s limit 1;" % (table_name, condition, query_date, order)

    ret_val, data = db_info.tsd_info_select(status, table_name, sql_stmt)
    return [ret_val, data]

# ------------------------------------------------------------------------------
# Get the last row in the table
# ------------------------------------------------------------------------------
def get_endpoint_tsd_row(status, table_name, is_first):

    if is_first:
        sql_stmt = "select file_id from %s order by file_id asc limit 1;" % table_name
    else:
        # get last
        sql_stmt = "select file_id from %s order by file_id desc limit 1;" % table_name

    ret_val, tsd_data = db_info.tsd_info_select(status, table_name, sql_stmt)

    if not ret_val:
        row_id = result_to_row_id(tsd_data)
    else:
        row_id = 0
    return [ret_val, row_id]
# ------------------------------------------------------------------------------
# Get the row ID from a query result set returning a single row
# ------------------------------------------------------------------------------
def result_to_row_id(tsd_data):

    if not len(tsd_data):
        row_id = 0
    else:
        row_id = tsd_data[0][0]

    return row_id

# ------------------------------------------------------------------------------
# Query the diff between the start_id and the end_id
# ------------------------------------------------------------------------------
def query_difference(status, table_name, start_id, end_id):
    sql_stmt = "select count(*) from %s where file_id >= %s and file_id <= %s;" % (table_name, start_id, end_id)
    ret_val, tsd_data = db_info.tsd_info_select(status, table_name, sql_stmt)
    if not ret_val:
        # Get the count from the select statement
        if not len(tsd_data):
            count = 0
        else:
            count = tsd_data[0][0]
        # the number of files missing
        diff = end_id - start_id + 1 - count

    else:
        diff = 0
    return [ret_val, diff]


# ------------------------------------------------------------------------------
# Place a row or a range in the message
# ------------------------------------------------------------------------------
def row_or_range_to_msg(rows_requested:list, table_name:str, row_needed:int, row_in_tsd:int, end_id:int, trace_level:int):
    
    if row_needed < row_in_tsd:
        # place the missing rows in the message
        if trace_level:
            utils_print.output("\r\n[Consumer] [%s] [Files Requested: %u] [%u-%u]" % \
                               (table_name, row_in_tsd - row_needed, row_needed, row_in_tsd), True)

        if row_in_tsd <= end_id:
            rows_requested.append((row_needed, row_in_tsd))
        else:
            # last batch request
            rows_requested.append((row_needed, end_id))
    else:
        row_needed = row_in_tsd

    return row_needed       # Return the first row added to buffer

# ------------------------------------------------------------------------------
# Push to message missing rows
# query_from - the first row requested in the SQL select to the TSD table
# end_id - the last row needed
# tsd_data - the rsult of the SQL query to the local TSD table
# ------------------------------------------------------------------------------
def update_request_msg(status, rows_requested, table_name, query_from, end_id, tsd_data, trace_level):
    global max_tsd_rows_

    first_row_missing = 0
    if not len(tsd_data):
        # TSD table is empty    - Request all rows
        first_row_missing = row_or_range_to_msg(rows_requested, table_name, query_from, end_id, end_id, trace_level)
        next_row = end_id
    else:
        
        # Consider the rows before the first row retrieved from the local TSD table
        row_in_tsd = int(tsd_data[0][0])     # The first row in the tsd table
        
        row_or_range_to_msg(rows_requested, table_name, query_from, row_in_tsd, end_id, trace_level)

        next_row = row_in_tsd
        
        # Consider the rows that were retrieved from the TSD table
             
        for entry in tsd_data:
            row_in_tsd = entry[0]
            
            if next_row == row_in_tsd:
                # This row exists in the local tsd -> consider the next row
                next_row += 1
                continue
            
            # place the missing rows in the message
            row_missing = row_or_range_to_msg(rows_requested, table_name, next_row, row_in_tsd, end_id, trace_level) # Push row or range of rows to the message
            if not first_row_missing:
                first_row_missing = row_missing

            next_row = row_in_tsd + 1

        # Consider the rows from the last row of the tsd
        if len(tsd_data) < max_tsd_rows_:
            # ask for all the rest
            if next_row < query_from + max_tsd_rows_:
                row_missing = row_or_range_to_msg(rows_requested, table_name, next_row, end_id, end_id, trace_level)
                next_row = end_id
                if not first_row_missing:
                    first_row_missing = row_missing

    # Return: first_row_missing = The first row which is needed
    # Return: next_row - all the rows up to the next_row were requested (note: next_row was not requested / included)
    return [first_row_missing, next_row]

# ------------------------------------------------------------------------------
# Request the missing files:
# Query the table to determine IDs whch are missing
# ------------------------------------------------------------------------------
def request_missing_files(status, table_name, start_id, end_id, ip, port, trace_level ):

    global process_mode_

    query_from = start_id               # The first ID that is needed to be considered
    first_row_missing = 0
    rows_requested = []                 # the list of rows to request
    
    while query_from < end_id:

        sql_stmt = "select file_id from %s where file_id >= %s and file_id <= %s order by file_id limit %u;" % (table_name, query_from, end_id, max_tsd_rows_)
        ret_val, tsd_data = db_info.tsd_info_select(status, table_name, sql_stmt)

        # return the first row that was considered to the last row considered (not including)
        missing_row, query_from = update_request_msg(status, rows_requested, table_name, query_from, end_id, tsd_data, trace_level)       # Push to message missing rows

        if not first_row_missing:
            first_row_missing = missing_row    # Save the first row considered

        if len(rows_requested) > 100 or not len(tsd_data):
            break           # Cap the size of the message or all files requested (if tsd_data is empty, process requested all IDs)


    if first_row_missing and len(rows_requested):
        if process_mode_ == "active":       # If mode is suspend, files are not requested

            # Make a string message
            if member_cmd.is_debug_method("consumer"):
                # Debug instruction may set a max on the files requested
                debug_cmd = member_cmd.get_debug_instructions("consumer")
                if "files" in debug_cmd:
                    rows_requested = minimize_files_requested(debug_cmd, rows_requested)

            message_rows = ""
            for entry in rows_requested:
                start_at = entry[0]
                end_at = entry[1]
                if (start_at + 1) == end_at:
                    message_rows += ',%s' % str(start_at)
                else:
                    message_rows += ',%s-%s' % (str(start_at), str(end_at))

            # send a message requesting a list of files (by their TSD row ID)
            member_cmd.send_message(0, status, ip, int(port), mem_view_, "file deliver %s" % table_name, message_rows[1:], message_header.BLOCK_INFO_AUTHENTICATE)
    else:
        if trace_level:
            utils_print.output("\r\n[Consumer] [%s] [No file missing] [Validated row: %u]" % (table_name, end_id), True)

        first_row_missing = end_id + 1

    return [ret_val, first_row_missing]

# ------------------------------------------------------------------------------
# Create TSD table for new operators
# ------------------------------------------------------------------------------
def create_tsd_tables(status, node_member_id, operators_list):

    for operator in operators_list:

        member_id = operator[0]
        if member_id != node_member_id:
            # Not this node
            # The call only creates if the table does not exists
            db_info.create_member_tsd(status, node_member_id, member_id)

# ------------------------------------------------------------------------------
# Request an update from the member nodes on the last status of the TSD table
# The event message send: "run client ip:port event get_recent_tsd_info tsd_id date_start date_end"
# this call triggers a process on a target machine at events.get_recent_tsd_info
# ------------------------------------------------------------------------------
def event_request_tsd_update(status, data_buffer, operators_list, start_date, end_date):

    global info_tsd_msg
    global active_peers_        # The number of peers that received a meesage

    message_send = 0
    for operator in operators_list:

        info_tsd_msg[2] = operator[1] + ":" + str(operator[2])
        info_tsd_msg[-3] = "tsd_%s" % operator[0]
        if not start_date:
            start_date = '0'
        else:
            info_tsd_msg[-2] = start_date
        if not end_date:
            info_tsd_msg[-1] = '0'
        else:
            info_tsd_msg[-1] = end_date

        # Message includes table-name, start-date, end-date
        ret_val = member_cmd.run_client(status, data_buffer, info_tsd_msg, 0)  # --> message: get_recent_tsd_info triger a reply message: ha.recent_tsd_info
        if not ret_val:
            message_send += 1

    active_peers_ = message_send


# ------------------------------------------------------------------------------
# For debug - Change the number of files requested using the command:
# debug on consumer files = 5
# To change the files requested to 5 and set the mode afterwards to "suspend"
# ------------------------------------------------------------------------------
def minimize_files_requested(debug_cmd, files_requested):   # DEBUG CODE

    global process_mode_

    if len (debug_cmd) >= 6 and debug_cmd[3] == "files" and debug_cmd[4] == "=" and debug_cmd[5].isdecimal():
        max_files = int(debug_cmd[5])
        files_list = []           # change the requests for files

        for files_range in files_requested:
            start_id, end_id = files_range
            range_diff = end_id - start_id
            if range_diff >= max_files:
                files_list.append((start_id, start_id + max_files))
                break       # at the max files that will be requested
            files_list.append(files_range)
            max_files -= range_diff
    else:
        files_list = files_requested

    process_mode_ = "suspend"       # Stop until mode is changed to "active"

    return files_list
