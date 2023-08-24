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
import anylog_node.generic.utils_print as utils_print
import anylog_node.tcpip.message_header as message_header
import anylog_node.generic.utils_io as utils_io
import anylog_node.generic.utils_columns as utils_columns
import anylog_node.generic.params as params
import anylog_node.blockchain.metadata as metadata


MAX_FILES_LIST = 10
files_transferred = []
files_counter = 0  # number of files transferred
files_next = 0  # Location in the files_transferred list

distr_running_flag = False

# ------------------------------------------------------------------------------
# Test if the data distributor is running
# ------------------------------------------------------------------------------
def is_distr_running():
    return distr_running_flag

# ------------------------------------------------------------------------------
# 1) Transfer files to members of the cluster
# 2) Move the files to archival
#  Example: run data distributor
# ------------------------------------------------------------------------------
def data_distributor(dummy: str, conditions: dict):

    global distr_running_flag

    process_status.reset_exit("distributor")

    status = process_status.ProcessStat()

    file_types = ["json", "backup", "gz"]  # JSON files are with the Source Data and Archive files are with partition data

    distr_dir = interpreter.get_one_value_or_default(conditions, "distr_dir", "!distr_dir") + params.get_path_separator()
    archive_dir = interpreter.get_one_value_or_default(conditions, "archive_dir", "!archive_dir")
    err_dir = interpreter.get_one_value_or_default(conditions, "err_dir", "!err_dir")

    is_compress = True

    distr_running_flag = True

    metadata_version = 0

    while 1:

        file_list = []  # needs to be inside the while loop to be initiated (as the same file will be called again)

        trace_level = member_cmd.commands["run data distributor"]['trace']

        ret_val, file_name = member_cmd.get_files_from_dir(status, "distributor", 5, distr_dir, "file", file_types, file_list, None, None, False)
        if ret_val:
            # Including Publisher terminated - or global termination
            break

        # Get the list of destination operators
        if not metadata.test_metadata_version(metadata_version):
            # if the metadata version was changed, Load the metadata
            ret_val = member_cmd.blockchain_load(status, ["blockchain", "get", "cluster"], False, 0)
            if ret_val:
                # move the file to error dir as metadata failed to load
                extended_name = "err_%u" % ret_val
                if not utils_io.file_to_dir(status, err_dir, file_name, extended_name, True):
                    break           # Failed to move to error dir
                continue            # Get the next file

            operators_list = metadata.get_operators_info(status, None, False, ["ip", "port"])     # Get the IP + Ports excluding this Operator
            metadata_version = metadata.get_metadata_version()


        if file_name[-3:] == ".gz":
            source_file = file_name
            file_compressed = True
        elif is_compress:
            # compress the file
            ret_val = utils_io.compress(status, file_name)
            if ret_val:
                break       # compression failed
            if not utils_io.delete_file(file_name):   # delete the uncompressed file
                ret_val = process_status.Failed_to_delete_file
                break
            
            source_file = file_name + ".gz"
            file_compressed = True
           
        else:
            source_file = file_name
            file_compressed = False

        # copy the file to one or more standbys -> GENERIC_USE_WATCH_DIR will place the file in the watch and unzip
        ret_val = member_cmd.transfer_file(status, operators_list, source_file, "",  message_header.GENERIC_USE_WATCH_DIR, trace_level, "Distributor", False)
        if ret_val:
            break


        # Move the file to archive + compress -> if archiving fails - move to err_dir
        ret_val = utils_io.archive_file(status, "json", archive_dir, err_dir, file_name, not file_compressed)
        if ret_val:
            break

        keep_statistics(file_name)  # Keep statistics on files transferred

    process_log.add_and_print("event", "HA Distributor process terminated: %s" % process_status.get_status_text(ret_val))
    distr_running_flag = False


# -----------------------------------------------------------------
# Keep statistics on files transferred
# -----------------------------------------------------------------
def keep_statistics(dest_file_name):
    global MAX_FILES_LIST
    global files_transferred
    global files_counter
    global files_next

    if len(files_transferred) == MAX_FILES_LIST:
        files_transferred[files_next] = (dest_file_name, utils_columns.get_current_time())
    else:
        files_transferred.append((dest_file_name, utils_columns.get_current_time()))
    files_counter += 1
    files_next += 1
    if files_next >= 10:
        files_next = 0  # reset location in the list
# -----------------------------------------------------------------
# Show info on  the HA process
# -----------------------------------------------------------------
def show_distr_info():

    global files_transferred
    global files_counter

    info_str = ""

    info_str += "\r\nFiles Transferred: %u" % files_counter

    if files_counter:
        info_str += utils_print.output_nested_lists(files_transferred, "Last Files Trahnferred", ["File", "Time"], True)

    return info_str




