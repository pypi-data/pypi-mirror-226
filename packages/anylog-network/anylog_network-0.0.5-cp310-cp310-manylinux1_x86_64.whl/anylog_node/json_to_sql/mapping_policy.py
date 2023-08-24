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

try:
    import base64
except:
    base64_installed_ = False
else:
    base64_installed_ = True

try:
    import cv2
except:
    cv2_installed_ = False
else:
    cv2_installed_ = True

try:
    import numpy
except:
    numpy_installed_ = False
else:
    numpy_installed_ = True

try:
    import ast
except:
    ast_installed_ = False
else:
    ast_installed_ = True



import sys
import anylog_node.generic.utils_json as utils_json
import anylog_node.generic.utils_columns as utils_columns
import anylog_node.generic.utils_data as utils_data
import anylog_node.generic.utils_print as utils_print
import anylog_node.generic.params as params
import anylog_node.generic.process_status as process_status
import anylog_node.generic.utils_io as utils_io
import anylog_node.dbms.partitions as partitions
import anylog_node.dbms.db_info as db_info

mapping_trace_ = 0      # Updated using the command: trace level = 1 mapping


# ==================================================================
# Set the trace level to show the mapping process
# command: trace level = 1 mapping
# ==================================================================
def set_mapping_trace(trace_level):
    global mapping_trace_

    mapping_trace_ = trace_level

# ==================================================================
#
# Get columns list from the mapping policy
# Update a dictionary:
#           with column type as f(column name)
# ==================================================================
def policy_to_columns_dict(status, dbms_name, table_name, instruct, columns):
    '''
    instruct - the mapping policy
    columns - a dictionary to be updated with the info
    '''

    if not "mapping" in instruct or not isinstance(instruct["mapping"], dict):
        if "id" in instruct:
            policy_id = instruct["id"]
        else:
            policy_id = ""
        status.add_error("Policy provided '%s' is not of type 'mapping'" % (policy_id))
        return process_status.ERR_wrong_json_structure

    policy_inner = instruct["mapping"]

    if not "schema" in policy_inner or not isinstance(policy_inner["schema"], dict):
        if "id" in instruct:
            policy_id = instruct["id"]
        else:
            policy_id = ""

        status.add_error("Missing 'schema' in mapping policy '%s'" % (policy_id))
        return process_status.ERR_wrong_json_structure


    ret_val = process_status.SUCCESS

    schema = policy_inner["schema"]

    for column_name, column_data in schema.items():

        if isinstance(column_data, dict):
            column_list = [column_data]  # Make a list with one attribute
        elif isinstance(column_data, list):
            # Multiple dictionaries in the list
            column_list = column_data
        else:
            policy_id = policy_inner["id"] if "id" in policy_inner else ""
            status.add_error("Wrong column info in 'schema' in mapping policy '%s'" % (policy_id))
            ret_val = process_status.ERR_wrong_json_structure
            break

        for column_info in column_list:     # May have multiple options

            if "type" in column_info:
                if "dbms" in column_info and column_info["dbms"] != dbms_name:
                    continue               # Incorrect option, get to the next option
                if "table" in column_info and column_info["table"] != table_name:
                    continue               # Incorrect option, get to the next option
                data_type = column_info["type"].lower()

                if "default" in column_info.keys():
                    default_value = column_info["default"]
                    if default_value:
                        data_type = "%s NOT NULL DEFAULT %s" % (data_type, default_value)

                ret_val, unified_data_type = utils_data.unify_data_type( status, data_type )
                if ret_val:
                    break

                columns[column_name] = unified_data_type.upper()
                break           # Data type that satisfies the dbms and table was found

            if ret_val:
                break

    return ret_val

# ----------------------------------------------------------------------------------------
# Map the source data by the policy schema
# ----------------------------------------------------------------------------------------
def apply_policy_schema(status, dbms_name, table_name, policy_inner, policy_id, json_data, is_dest_string, blobs_dir):
    '''
    status - status object
    dbms_name - used to extract the schema if the table is not declared
    table_name - used to extract the schema if the table is not declared
    policy_inner - a dictionary with an attribute "schema"
    policy_id - the ID of the policy
    readings - the source data organized as a list
    dest_string - if True, returns a list of JSON strings, if False, returns a list of JSON objects
    blobs_dir - the directory to write the blob data
    '''

    global tables_schemas_
    global mapping_trace_

    if blobs_dir and blobs_dir[-1] != params.get_path_separator():
        blobs_dir += params.get_path_separator()

    data_source = "0"
    insert_list = None

    if not "schema" in policy_inner or not isinstance(policy_inner["schema"], dict):
        status.add_error("Missing 'schema' in mapping policy '%s'" % (policy_id))
        ret_val = process_status.ERR_wrong_json_structure
        insert_list = None
    else:
        ret_val = process_status.SUCCESS
        schema = policy_inner["schema"]

        if "source" in policy_inner:
            # Get the data source - i.e of a device generating the data (data source is used in the file name)
            source_info = policy_inner["source"]
            ret_val, data_source = bring_and_default_to_data(status, source_info, policy_id, "source", json_data)
            if not data_source or not isinstance(data_source, str):
                data_source = '0'
            else:
                data_source = data_source.lower().replace(' ', '_') # Make lower case + no spaces

        file_name_prefix = f"{dbms_name}.{table_name}."

        if not ret_val:

                # A key (from the schema) to pull a list of readings from the message
            ret_val, readings_key = get_policy_info(status, policy_inner, policy_id, "readings", False)
            if ret_val:
                # there is no list, just the json msg
                if isinstance(json_data, list):
                    readings = json_data
                else:
                    readings = [json_data]
                ret_val = process_status.SUCCESS        # The entire JSON representa a reading
            else:
                if not readings_key in json_data:
                    status.add_error("Missing '%s' in mapping policy '%s'" % (readings_key, policy_id))
                    ret_val = process_status.ERR_wrong_json_structure
                else:
                    readings = json_data[readings_key]
                    if not isinstance(readings, list):
                        readings = [readings]       # May have a single dictionary - not in a list -Make a list with a single entry

        if partitions.is_partitioned(dbms_name, table_name):
            par_info = partitions.get_par_info(dbms_name, table_name)
            column_name = par_info[2]  # The name of the column that makes the partition
            if column_name != "insert_timestamp":
                # insert_timestamp is added during the mapping of JSON to Insert and does not need to be included on the policy
                if not column_name in schema:
                    status.add_error(f"Policy '{policy_id}' for table '{dbms_name}.{table_name}' is missing partitioned column: '{column_name}'")
                    ret_val = process_status.Wrong_policy_structure

        if not ret_val:

            insert_list = []  # Make a list of rows from the topic info

            if not len(readings):
                # Empty readings
                readings = [{}]     # This setup would loop over the schema as an entry can be created from the root of the readings

            for index, data_entry in enumerate(readings):  # data_entry is one reading from a list of readings

                for attr_name, attr_data in schema.items():
                    # Go over all the columns in the schema and extract the data

                    if isinstance(attr_data, dict):
                        attr_list = [attr_data]         # Make a list with one attribute
                    elif isinstance(attr_data, list):
                        # Multiple dictionaries in the list
                        attr_list = attr_data
                    else:
                        status.add_error("Wrong column info in 'schema' in mapping policy '%s'" % (policy_id))
                        ret_val = process_status.ERR_wrong_json_structure
                        break

                    is_apply = 0
                    for column_info in attr_list:
                        # Because of condition, could have multiple column infos for a single attr_name
                        if is_apply:
                            # The if condition returned True and the column_info was processed
                            break
                        if "dbms" in column_info and column_info["dbms"] != dbms_name:
                            continue  # Incorrect option, get to the next option
                        if "table" in column_info and column_info["table"] != table_name:
                            continue  # Incorrect option, get to the next option

                        if not isinstance(column_info, dict):
                            status.add_error("Schema info is not in a dictionary format in mapping policy '%s'" % (policy_id))
                            ret_val = process_status.ERR_wrong_json_structure
                            break

                        if "condition" in column_info:
                            is_apply = process_if_code(status, column_info, policy_id, "condition", data_entry)
                            if is_apply == -1:
                                # Failed to process if
                                ret_val = process_status.ERR_wrong_json_structure
                                break
                            if not is_apply:  # 0 value means condition failed
                                continue  # Test next column

                        ret_val, data_type = get_policy_info(status, column_info, policy_id, "type", True)
                        if ret_val:
                            break

                        source_attr_name = attr_name
                        if "value" in column_info:
                            ret_val, bring_cmd = get_policy_info(status, column_info, policy_id, "value", True)
                            if ret_val:
                                break
                            if bring_cmd[:5] == "bring" and len(bring_cmd) >= 8 and (bring_cmd[5] == ' ' or bring_cmd[5] == '['):
                                # find the key in the source data
                                bring_cmd = bring_cmd[5:].strip()
                                if  len(bring_cmd) >= 3 and bring_cmd[0] == '[' and bring_cmd[-1] == ']':
                                    source_attr_name = bring_cmd[1:-1]      # Get the attribute name from the bring command
                                else:
                                    status.add_error(f"Wrong BRING command in value associated with attribute {attr_name} in mapping policy {policy_id}")
                                    ret_val = process_status.ERR_wrong_json_structure
                                    break

                        if "root" in column_info and isinstance(column_info["root"], bool) and column_info["root"] == True:
                            # Take the info from a different the root (rather than the reading instance)
                            ret_val, attr_val = bring_and_default_to_data(status, column_info, policy_id, source_attr_name, json_data)
                        else:
                            ret_val, attr_val = bring_and_default_to_data(status, column_info, policy_id, source_attr_name, data_entry)

                        if ret_val:
                            break

                        if "blob" in column_info and isinstance(column_info["blob"], bool) and column_info["blob"] == True:
                            # This is a file/blob column

                            # 1) Write the blob in the blobs dir
                            # 2) Calculate the hash value to use as the file name + place on the SQL table if column
                            #    includes:     hash = true

                            if not blobs_dir:
                                status.add_error(f"Missing blob dir definition when policy '{policy_id}' is processed")
                                ret_val = process_status.Blobs_dir_does_not_exists
                                break

                            ret_val, hash_type = get_policy_info(status, column_info, policy_id, "hash", True)
                            if ret_val:
                                break
                            if isinstance(hash_type, str) and hash_type == "md5":
                                #  - the hash value string is added to the relational table

                                hash_value = utils_data.get_string_hash('md5', attr_val, dbms_name + '.' + table_name)
                            else:
                                status.add_error(f"Policy '{policy_id}' includes Hash Type '{hash_type}' which is not recognized")
                                ret_val = process_status.Wrong_policy_structure
                                break

                            if "extension" in column_info and isinstance(column_info["extension"], str):
                                extension = column_info["extension"]    # The file type (added to the hash value)
                            else:
                                extension = None

                            if "apply" in column_info:
                                apply = column_info["apply"]    # Apply encoding or decoding
                            else:
                                apply = None


                            ret_val, column_val = blob_to_file(status, file_name_prefix, hash_value, attr_val, blobs_dir, extension, apply)
                            if ret_val:
                                break

                            policy_inner["bwatch_dir"] = True

                        else:
                            if "apply" in column_info:
                                # Apply a function on the value
                                ret_val, column_val = get_applied_val(status, column_info["apply"], attr_val)
                                if ret_val:
                                    break
                            else:
                                column_val = attr_val

                        ret_val, unified_data_type = utils_data.unify_data_type(status, data_type)
                        if ret_val:
                            break


                        # add column to the relational table
                        ret_val = add_column_to_list(status, insert_list, index, attr_name, unified_data_type, column_val, None, is_dest_string)
                        if ret_val:
                            break

                    if ret_val:
                        break

                if ret_val:
                    break

    if mapping_trace_:
        # Show the process output (the mapped data)
        show_insert_list(ret_val, insert_list)


    return [ret_val, data_source, insert_list]
# ----------------------------------------------------------------------
# Show the insert list if user specified:  trace level = 1 mapping
# ----------------------------------------------------------------------
def show_insert_list(ret_val, insert_list):
    # Show the process output (the mapped data)
    if ret_val:
        utils_print.output("\nMapping failed with error %u: %s" % (ret_val, process_status.get_status_text(ret_val)),
                           True)
    else:
        for entry in insert_list:
            utils_print.struct_print(entry, True, True, 1000)


# ----------------------------------------------------------------------
# Write blob data to a file
# ----------------------------------------------------------------------
def blob_to_file(status, file_name_prefix, hash_value, blob_data, blobs_dir, file_type, apply):
    '''
    The file name (written on disk) includes a prefix of dbms+table+source+hash+type
    The hash+type are returned and written in the data row
    apply - can be base64decoding
    '''

    ret_val = process_status.SUCCESS
    if not blobs_dir:
        blob_file_name = None
        status.add_error("Missing blobs directory in global dictionary (!blobs_dir)")
        ret_val = process_status.Missing_key_in_dictionary
    else:
        # Write blob file
        blob_file_name = hash_value if not file_type else hash_value + '.' + file_type

        if apply:
            if apply == "base64decoding":
                if not base64_installed_:
                    status.add_error(f"Failed to import base64 library")
                    ret_val = process_status.Failed_to_import_lib
                else:
                    try:
                        base64_bytes = blob_data.encode('ascii')
                        blobs_info = base64.b64decode(base64_bytes)
                    except:
                        status.add_error(f"Failed to apply Base64 decoding on data")
                        ret_val = process_status.Failed_to_encode_data
            elif apply == "opencv":
                if not numpy_installed_:
                    status.add_error(f"Failed to import Numpy library")
                    ret_val = process_status.Failed_to_import_lib
                elif not cv2_installed_:
                    status.add_error(f"Failed to import OpenCV library")
                    ret_val = process_status.Failed_to_import_lib
                elif not ast_installed_:
                    status.add_error(f"Failed to import ast library")
                    ret_val = process_status.Failed_to_import_lib
                else:
                    try:
                        if not isinstance(blob_data, numpy.ndarray) or not isinstance(blob_data, list):
                            content = ast.literal_eval(blob_data)
                        else:
                            content = blob_data

                        if not isinstance(content, numpy.ndarray):
                            ndarry_content = numpy.array(content)  # convert back to numpy.ndarray
                        else:
                            ndarry_content = content
                    except:
                        status.add_error(f"Failed to apply OpenCV decoding on data")
                        ret_val = process_status.Failed_to_encode_data
            else:
                blobs_info = blob_data
        else:
            blobs_info = blob_data

        if not ret_val:
            file_path_name = blobs_dir + file_name_prefix + blob_file_name

            if apply == "opencv":
                try:
                    ret_code = cv2.imwrite(file_path_name, ndarry_content)
                except:
                    errno, value = sys.exc_info()[:2]
                    message = "Failed to write file: '%s' with error %s: %s" % (file_path_name, str(errno), str(value))
                    status.add_error(message)
                    ret_val = process_status.File_write_failed
                    ret_code = True     # Avoid the second error message below

            elif isinstance(blobs_info,bytes):
                ret_code = utils_io.write_data_block(file_path_name, True, blobs_info)
            else:
                ret_code = utils_io.write_str_to_file(status, blob_data, file_path_name)

            if not ret_code:
                status.add_error("Failed to write blob data to blobs dir at: %s" % blobs_dir + file_name_prefix + blob_file_name)
                ret_val = process_status.File_write_failed


    return [ret_val, blob_file_name]


# ----------------------------------------------------------------------
# Apply a function on the value
# ----------------------------------------------------------------------
def get_applied_val(status, applied_func, attr_val):

    value = None
    ret_val = process_status.SUCCESS
    if applied_func == "epoch_to_datetime":
        # Convert Epoch to datetiime
        value = utils_columns.epoch_to_date_time(attr_val)
        if not value:
            message = f"Failed to apply mapping using function '{applied_func}' on value: {str(attr_val)}"
            status.add_error(message)
            ret_val = process_status.Wrong_policy_structure
    else:
        message = f"Unrecognized mapping function '{applied_func}' on value: {str(attr_val)}"
        status.add_error(message)
        ret_val = process_status.Wrong_policy_structure

    return [ret_val, value]
# ----------------------------------------------------------------------
# Use the bring command to get the attribute value. If the bring doesn't
# return data - use the default key.
# If bring is available - place the compiled bring in the policy for next time usage
# ----------------------------------------------------------------------
def bring_and_default_to_data(status, column_info, policy_id, attr_name, data_entry):

    ret_val, bring_cmd = utils_json.get_policy_val(status, column_info, policy_id, "bring", str, True, False)
    if not ret_val:
        if "compiled_bring" in column_info:
            # get the bring command which was already processed using utils_data.cmd_line_to_list_with_json
            bring_list = column_info["compiled_bring"]
        else:
            if not bring_cmd:
                bring_cmd = "[%s]" % attr_name  # Use the attribute name to bring the data

            bring_list, left_brackets, right_brakets = utils_data.cmd_line_to_list_with_json(status, bring_cmd, 0, 0)
            if left_brackets != right_brakets:
                status.add_error("Wrong bring command in column '%s' in mapping policy '%s'" % (attr_name, policy_id))
                ret_val = process_status.ERR_wrong_json_structure
            else:
                column_info["compiled_bring"] = bring_list  # save for next row

    if not ret_val:
        ret_val, attr_val = utils_json.pull_info(status, [data_entry], bring_list, None, 0)
        if not ret_val and attr_val == "":
            # Get the default
            ret_val, attr_val = utils_json.get_policy_val(status, column_info, policy_id, "default", None, True,  False)
            if not ret_val:

                if attr_val == None:
                    status.add_error(
                        "Failed to extract value from data and no default value in policy schema, policy id: '%s'" % policy_id)
                    ret_val = process_status.ERR_wrong_json_structure
                else:
                    if isinstance(attr_val, str) and attr_val == "now()":
                        attr_val = utils_columns.get_current_utc_time()

    return [ret_val, attr_val]
# ----------------------------------------------------------------------
# Process AnyLog code on the policy
# In the first call - analyze_if is called and stored on the policy such that it is available to reuse.
# ----------------------------------------------------------------------
def process_if_code(status, mapping, policy_id, key, json_msg):
    '''
    status - object status
    mapping - a dictionary with the if statement
    policy_id - the id of the policy with the if statement
    key - the key to retieve the if statement
    json_msg - The dictionary with the data to validate
    '''

    compiled_key = "compiled_%s" % key

    if not compiled_key in mapping:
        if_stmt = mapping[key]
        conditions_list = []
        cmd_words, left_brackets, right_brakets = utils_data.cmd_line_to_list_with_json(status, if_stmt, 0, 0)  # a list with words in command line
        if left_brackets != right_brakets:
            process_status.add_error("Policy [%s] is missing braket in the %s statement" % (policy_id, key))
            return -1

        ret_val, offset_then, with_paren = params.analyze_if(status, cmd_words, 0, conditions_list)
        if ret_val:
            return -1
        mapping[compiled_key] = (cmd_words, offset_then, with_paren, conditions_list)   # save for next time
    else:
        cmd_words, offset_then, with_paren, conditions_list =  mapping[compiled_key]


    # test_condition returns: a) offset to then, b) 0 (False), 1 (True), -1 (Error)
    next_word, ret_code = params.process_analyzed_if(status, cmd_words, 0, offset_then, with_paren, conditions_list, json_msg)

    return ret_code


# ----------------------------------------------------------------------
# Get info from Policy
# ----------------------------------------------------------------------
def get_policy_info(status, json_obj, policy_id, key, must_exists):

    if key in json_obj:
        ret_val = process_status.SUCCESS

        policy_value = json_obj[key]
        if isinstance(policy_value,str) or isinstance(policy_value,bool):
            value = policy_value
        elif isinstance(policy_value,dict):
            # get the BRING command
            ret_val, value = get_policy_info(status, policy_value, policy_id, "bring", True)
            if not ret_val and not isinstance(value,str):
                ret_val = process_status.ERR_wrong_json_structure
    else:
        ret_val = process_status.ERR_wrong_json_structure


    if ret_val:
        value = None
        if must_exists:
            status.add_error("Missing info for attribute '%s' in mapping policy '%s'" % (key, policy_id))


    return [ret_val, value]


# ----------------------------------------------------------------------
# Given a list of column values, add a new column value to the list
# Attr constant could be a repeatable date using the key now
# ----------------------------------------------------------------------
def add_column_to_list(status, insert_list, index, bring_attr_name, data_type, attr_val, attr_constant, is_dest_string):
    '''
    bring_attr_name is the name set in the bring command.
    If the brings pulls a dictionary with name and value, the attribute name is modified by the dictionary in
    the method get_formatted_val

    dest_string - if True, returns a list of JSON strings, if False, returns a list of JSON objects
    '''

    ret_val, column_val_str, dict_attr_name = get_formatted_val(status, data_type, attr_val)
    attr_name = dict_attr_name or bring_attr_name

    if not ret_val:
        if index >= len(insert_list):
            # A new entry to the list
            if is_dest_string:
                # Organize as a string
                if attr_constant:
                    insert_list.append(attr_constant + "\"" + attr_name + "\":" + column_val_str + "}")
                elif data_type == "timestamp":
                    insert_list.append("{\"" + attr_name + "\":\"" + column_val_str + "\"}")    # added because of now()
                else:
                    insert_list.append( "{\"" + attr_name + "\":" + column_val_str + "}" )
            else:
                # Organize as object
                insert_list.append( { attr_name : column_val_str })
        else:
            if is_dest_string:
                if data_type == "timestamp":
                    insert_list[index] = insert_list[index][:-1] + "," + "\"" + attr_name + "\":\"" + column_val_str + "\"}"
                else:
                    insert_list[index] = insert_list[index][:-1] + "," + "\"" + attr_name + "\":" + column_val_str + "}"
            else:
                insert_list[index] [attr_name] =  column_val_str

    return ret_val
# ----------------------------------------------------------------------
# Format the value string by the data type
# ----------------------------------------------------------------------
def get_formatted_val(status, data_type, pulled_val):
    ret_val = process_status.SUCCESS
    value_str = None
    time_str = None

    if isinstance(pulled_val,str) and len(pulled_val) > 3 and pulled_val[0] == '{' and pulled_val[-1] == '}':
        json_dict = utils_json.str_to_json(pulled_val)
        if json_dict:
            # a dictionary with a name - value pair
            attr_name = next(iter(json_dict))      # Get the name from the JSON dictionary
            attr_val = json_dict[attr_name]
            attr_name = utils_data.reset_str_chars(attr_name.lower())
        else:
            attr_name = None
            attr_val = pulled_val
    else:
        attr_name = None
        attr_val = pulled_val

    if data_type.startswith("varchar") or data_type == "uuid":
        value_str = "\"%s\"" % attr_val
    elif data_type == "int":
        value_str = str(attr_val)
    elif data_type == "float":
        value_str = str(attr_val)
        if 'e' in value_str:
            # Change scientific notation
            if utils_data.isfloat(value_str):
                value_str = str(float(value_str))

    elif data_type == "timestamp":
        if isinstance(attr_val, str):
            if attr_val.isdecimal():
                time_val = int(attr_val)
            elif attr_val.isdigit():
                time_val = int(float(attr_val))
            else:
                time_val = None
                if len(attr_val) > 10 and attr_val[-3] == ':' and (attr_val[-6] == '+' or attr_val[-6] == '-'):
                    # Format like: '2011-11-04T00:05:23+04:00' - https://docs.python.org/3/library/datetime.html
                    time_str = utils_columns.time_iso_format(attr_val)
                else:
                    time_format =  utils_columns.get_utc_time_format(attr_val)
                    if utils_columns.validate_date_string(attr_val, time_format):
                        time_str = attr_val
                    else:
                        time_format = utils_columns.get_local_time_format(attr_val)
                        if utils_columns.validate_date_string(attr_val, time_format):
                            time_str = attr_val
                        else:
                            time_str = None

        elif isinstance(attr_val, int):
            time_val = attr_val
        elif isinstance(attr_val, float):
            time_val = int(attr_val)
        else:
            time_val = None

        if time_val:
            # Map second to time string
            seconds = int(time_val/1000)
            time_str = utils_columns.seconds_to_date(seconds)


        if not time_str:
            status.add_error("MQTT failure: Failed to retrieve date and time from message attribute value: %s" % str(attr_val))
            ret_val = process_status.MQTT_info_err
        else:
            value_str = time_str
    elif data_type == "bool":
        value_str = str(attr_val).lower()
    else:
        value_str = str(attr_val)

    return [ret_val, value_str, attr_name]

# ----------------------------------------------------------------------
# Validate the policy structure
# ----------------------------------------------------------------------
def validate(status, policy):

    ret_val = process_status.ERR_wrong_json_structure
    if not isinstance(policy,dict):
        status.add_error("Error in policy structure")
    elif not "mapping" in policy:
        status.add_error("Mapping policy does not include the key 'mapping' in the root")
    else:
        policy_inner = policy["mapping"]
        if not "id" in policy_inner:
            status.add_error("Mapping policy without an ID")
        elif not "schema" in policy_inner:
            status.add_error("Mapping policy without a schema")
        else:
            ret_val = process_status.SUCCESS

    return ret_val


# ------------------------------------------------------------------------------
# Archive blob fIle
# Write to a DBMS, move file to archive directory
# ------------------------------------------------------------------------------
def archive_blob_file(status, dbms_name, table_name, blob_data):

    blobs_dir = params.get_value_if_available("!blobs_dir")
    err_dir = params.get_value_if_available("!err_dir")
    blob_file_name = ""
    if not blobs_dir or not err_dir:
        if not blobs_dir:
            status.add_error("Missing blobs directory in global dictionary (!blobs_dir)")
        else:
            status.add_error("Missing error directory in global dictionary (!err_dir)")
        ret_val = process_status.Missing_key_in_dictionary
    else:
        if blobs_dir[-1] != params.get_path_separator():
            blobs_dir += params.get_path_separator()
        if err_dir[-1] != params.get_path_separator():
            err_dir += params.get_path_separator()


        file_name_prefix = f"{dbms_name}.{table_name}."
        blob_hash_value = utils_data.get_string_hash('md5', blob_data, dbms_name + '.' + table_name)
        # Write the blob to a blob dir and return the ID of the blob
        ret_val, blob_file_name = blob_to_file(status, file_name_prefix, blob_hash_value, blob_data, blobs_dir,
                                                            "blob", None)
        if not ret_val:
            # Insert the Blob to a DBMS
            utc_time = utils_columns.get_current_utc_time("%Y-%m-%dT%H:%M:%S.%fZ")
            date_time_key = utils_io.utc_timestamp_to_key(utc_time)
            db_info.store_file(status, "blobs_" + dbms_name, table_name, blobs_dir,
                                         blob_hash_value + '.blob', blob_hash_value, date_time_key[:6], True, 0)

            file_id_name = file_name_prefix + blob_file_name  # database + table + source + name

            absolute_name = blobs_dir + file_id_name

            # Move the file to archive + compress -> if archiving fails - move to err_dir
            ret_val = utils_io.archive_file(status, "*", blobs_dir, err_dir, absolute_name, False, date_time_key)
            if ret_val:
                status.add_keep_error("Failed to archive blob '%s.%s' " % (blobs_dir, file_id_name))

    return [ret_val, blob_file_name]



