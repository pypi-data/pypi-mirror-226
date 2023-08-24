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

# ------------------------------------------------------------------------
# Policy based permissions
# ------------------------------------------------------------------------
import anylog_node.cmd.member_cmd as member_cmd

import anylog_node.generic.process_status as process_status
import anylog_node.tcpip.message_header as message_header
import anylog_node.generic.process_log as process_log
import anylog_node.generic.utils_print as utils_print
import anylog_node.blockchain.al_auth as al_auth
import anylog_node.tcpip.net_utils as net_utils
import anylog_node.generic.utils_columns as utils_columns


# =======================================================================================================================
# 2 parts in authenticating a message:

# a) The message includes a proof that the user is the sender
# The proof includes the information + a signature:
# [Public Key] [Signature] [ip + port + time]

# b) The user is permitted to the process
# =======================================================================================================================

# =======================================================================================================================
# Authenticate the sender of a TCP message (the native AnyLog protocol)
# =======================================================================================================================
def authenticate_tcp_message(status, mem_view):
    '''
    Validate that the message was send in the last 10 minutes by the owner of the public key from the IP and  Port detailed in the message
    '''

    source_ip, source_port = message_header.get_source_ip_port(mem_view)

    ret_val, public_str = authenticate_message(status, mem_view, source_ip, str(source_port))

    if ret_val:
        if public_str:
            public_key_msg = f"using public key: {public_str}"
        else:
            public_key_msg = "public key not available"

        command = member_cmd.get_executable_command(status, None, mem_view)
        err_msg = "TCP server failed to authenticate the sender of a message (%s) from: %s:%u %s" % (command, source_ip, source_port, public_key_msg)
        process_log.add("Error", err_msg)
        if member_cmd.echo_queue:
            member_cmd.echo_queue.add_msg(err_msg)
        else:
            utils_print.output_box(err_msg)

    return [ret_val, public_str]

# =======================================================================================================================
# Authenticate REST message
# The sender was authenticated by the SSL protocol - place the user certificate public key in the status object
# =======================================================================================================================
def authenticate_rest_message(status, public_key):
    '''
    public key - derived from the certificate
    '''

    public_str = al_auth.get_public_key_chars(public_key)  # Remove the headers and new line
    if not public_str:
        err_msg = "REST server failed to identify the public key from a certificate"
        process_log.add("Error", err_msg)
        if member_cmd.echo_queue:
            member_cmd.echo_queue.add_msg(err_msg)
        else:
            utils_print.output_box(err_msg)

        ret_val = process_status.Failed_message_authentication
    else:
        status.set_public_key(public_str)
        ret_val = process_status.SUCCESS
    return ret_val

# =======================================================================================================================
# Permission process
# Given a member and a request - find the permissions policy of the member.
# From the permissions, determine the policies which are relevant to the request.
# Take the latest policy which is relevant and validate - if not validated, take the previous.
# Determine if the validated policy provides the needed permissions.
# =======================================================================================================================
def permission_process(status, depth, source, public_key, command, dbms_name, table_name):
    '''
    Status is the user status object
    source - the IP and port sending the message
    depth - counter to stop recursive calls
    command - command to validate
    '''

    if not public_key:
        status.add_error(f"Permission process for command '{command}' failed: missing public key")
        return False

    if depth > 5:
        status.add_error(f"Permission process for command '{command}' failed: recursive validation (hierarchy does not end with root user)")
        return False

    ret_code, permissions = permissions_by_public_key(status, public_key)
    if ret_code:
        return False

    permitted = False
    if len(permissions):
        # Test permissions for the command
        for entry in reversed(permissions):

            # Go over the permissions in reverse order - it can return +1 = allowed, -1 = revoked, 0 = ignored
            if dbms_name:
                ret_code = test_sql_permission(status, entry["permissions"], command, dbms_name, table_name)
            else:
                ret_code = test_process_permission(status, entry["permissions"], command)

            if ret_code == 1:
                # permission was found
                permitted = validation_process(status, depth + 1, source, entry, command, dbms_name, table_name)
                break
            if ret_code == -1:
                break

    if not permitted:
        if dbms_name:
            cmd_name = f"SQL on dbms '{dbms_name}' and table '{table_name}'"
        else:
            cmd_name = command

        err_msg = f"The public key provided is not authorized to execute the command: {cmd_name}, from: {source}, public key: {public_key}"
        status.add_error(err_msg)
        if command:
            # A call like: "get virtual tables" does not update message queue (as command is NULL, only dbms and table are provided).
            if  member_cmd.echo_queue:
                member_cmd.echo_queue.add_msg(err_msg)
            else:
                utils_print.output_box(err_msg)

    return permitted
# =======================================================================================================================
# Given the Public Key, Get the list of assignments (to permissions)
# For each assignment - get the permission ID
# For each permission ID - get the permissions
# =======================================================================================================================
def permissions_by_public_key(status, public_key):
    ret_val, assignments = assignments_by_public_key(status, public_key)
    permissions_list = []
    if not ret_val and len(assignments):
        assignment_list = assignments.split(',')
        for id in assignment_list:
            cmd_array = ["blockchain", "get", "permissions", "where", "id", "=", id]
            ret_val, permission = member_cmd.blockchain_get(status, cmd_array, "", True)
            if isinstance(permission, list) and len(permission):
                permissions_list.append(permission[0])  # The id is unique therefore permission will have a single entry

    return [ret_val, permissions_list]

# =======================================================================================================================
# Given the Public Key, Get the list of assignments (to permissions)
# =======================================================================================================================
def assignments_by_public_key(status, public_key):
    cmd_array = ["blockchain", "get", "assignment", "where", "members", "with", public_key, "bring",
                 "['assignment']['permissions']", "separator", "=", ","]
    ret_val, assignments = member_cmd.blockchain_get(status, cmd_array, "", True)
    if ret_val or not len(assignments):
        return [ret_val, assignments]
    return [ret_val, assignments]

# =======================================================================================================================
# Go over the permissions in reverse order - it can return +1 = allowed, -1 = revoked, 0 = ignored
# =======================================================================================================================
def test_process_permission(status, permissions, command):

    if "enable" in permissions.keys():
        enable = permissions["enable"]
    else:
        enable = None

    if "disable" in permissions.keys():
        disable = permissions["disable"]
    else:
        disable = None

    max_command_words = member_cmd.max_command_words
    command_words = command.split(' ',max_command_words)        # The words that make the command and can appear in a policy
    words_count = len(command_words)

    ret_val = -1  # only if explicitly allowed
    if not enable or '*' in enable:
        # all allowed
        ret_val = 1

        if not disable:
            return 1        # All allowed

    key_string = ""
    word_id = 0
    for index in range(words_count):
        cmd_word = command_words[index].strip()
        if not cmd_word:
            continue    # Empty word

        if word_id >= max_command_words:
            break

        key_string += cmd_word

        if enable and ret_val!= 1 and key_string in enable:
            ret_val = 1
            if not disable:
                return 1        # No disable

        if disable and ret_val!= -1 and key_string in disable:
            ret_val = -1
            if not enable:
                return -1      # no option to overwrite the -1

        key_string += ' '
        word_id += 1

    return ret_val  # return: 0 - not determined, 1 - allowed, -1 - not allowed

# =======================================================================================================================
# Validation process
# 1) Verify that the policy was signed using the public key value.
# 2) If the policy was signed by the root user, the policy is validated.
# 3) Verify that the the signer is authorized by validating the permission of the signer - call the permission process using the signer with the same request.
# =======================================================================================================================
def validation_process(status, depth, source, entry, command, dbms_name, table_name):
    '''
    Status is the user status object
    depth - counter to stop recursive calls
    source - the IP and port sending the message
    entry - A policy to validate
    command - command to validate
    '''

    # 1) Verify that the policy was signed using the public key value.
    if not member_cmd.authenticate(status, entry):
        ret_val = False
    else:

        # Get the public key of the root user
        get_cmd = "blockchain get member where type = root bring.first ['member']['public_key']"
        ret_value, root_public_key = member_cmd.blockchain_get(status, get_cmd.split(), "", True)

        if not root_public_key:
            err_msg = "Authentication Error: Missing root member policy"
            utils_print.output_box(err_msg)
            status.add_error(err_msg)
            ret_val = False
        else:

            # 2) If the policy was signed by the root user, the policy is validated.
            entry_public_key = entry['permissions']['public_key']
            if root_public_key == entry_public_key:
                ret_val = True
            else:
                # 3) Verify that the the signer is authorized by validating the permission of the signer - call the permission process using the signer with the same request.
                # Recursive call
                ret_val = permission_process(status, depth, source, entry_public_key, command, dbms_name, table_name)

    return ret_val

# =======================================================================================================================
# Go over the permissions in reverse order - it can return +1 = allowed, -1 = revoked, 0 = ignored
# =======================================================================================================================
def test_sql_permission(status, permissions, command, dbms_name, table_name):
    ret_val = 0  # not determined
    if "databases" in permissions.keys():
        databases = permissions["databases"]
    else:
        databases = None

    if "tables" in permissions.keys():
        tables = permissions["tables"]
    else:
        tables = None

    # Go over databases to determine permission
    if dbms_name and databases:
        for dbms in databases:
            if dbms == '*':
                ret_val = 1  # all databases allowed
            elif len(dbms) > 1 and dbms[0] == '-':
                # remove the database from the permissions - i.e.: '-lsl_demo'
                if dbms[1:] == dbms_name:
                    ret_val = -1  # database not allowd (-> test if specific table allowed)
                    break
            elif len(dbms) > 1 and dbms[0] == '+':
                # allow the database - i.e.: '+lsl_demo'
                if dbms[1:] == dbms_name:
                    ret_val = 1  # database allowd (-> test if specific table disabled)
                    break
            elif dbms == dbms_name:
                ret_val = 1  # database allowd (-> test if specific table disabled)
                break

    if tables and table_name and dbms_name:
        # table name needs to be prefixed by dbms name: dbms_name.table_name
        dbms_table = dbms_name + "." + table_name
        for table in tables:
            if len(table) > 1 and table[0] == '-':
                if table[1:] == dbms_table:
                    ret_val = -1  # table not allowd
                    break
            elif len(table) > 1 and table[0] == '+':
                if table[1:] == dbms_table:
                    ret_val = 1  # table allowed
                    break
            elif table == dbms_table:
                ret_val = 1  # table allowed
                break

    return ret_val
# =======================================================================================================================
# With a message in the following structure: [Public Key] [Signature] [ip + port + time]
# Authenticate the message as follows:
# 1) Test that the message was signed by the owner of the public key
# 2) Test that the IP and Port are signed
# 3) test that there is no more than 10 minutes difference to the sender time
# =======================================================================================================================
def authenticate_message(status, message, ip, port):

    auth_string = message_header.get_auth_str_decoded(message)

    if not auth_string:
        return [process_status.Failed_message_authentication, ""]

    # AUthentication string is split into 3:
    public_key, signature, signed_mesage = al_auth.unpack_auth_str(auth_string)

    index = signed_mesage.find("-")  # offset to the time

    if index <= 0:
        return [process_status.Failed_message_authentication, ""]

    # Signed message include IP and Port + Time

    ip_port = signed_mesage[:index]
    message_time = int(signed_mesage[index + 1:])

    if ip_port != ip + ':' + port:
        valid_ip = False
        index = ip_port.find(':')
        if index > 0:
            if (net_utils.get_external_ip() == ip_port[:index] and\
                index < (len(ip_port) + 1) and ip_port[index + 1:] == port):
                    # On the same network - replace the external ip with the local ip to see that IP and Port were properly signed
                    valid_ip = True
        if not valid_ip:
            status.add_error("Message Authentication Failure: IP and Port signed are different than destination Ip and port")
            return [process_status.Failed_message_authentication, ""]

    current_time = utils_columns.get_current_time_in_sec()

    if current_time > (message_time + 600) or current_time < (message_time - 600):
        # needs to see 10 minutes or less of a difference between the send time and receive time
        status.add_error("Message Authentication Failure: Authentication time interval expired")
        return [process_status.Failed_message_authentication, ""]

    if al_auth.verify(public_key, signature, signed_mesage):
        ret_val = process_status.SUCCESS
    else:
        ret_val = process_status.Failed_message_authentication

    return [ret_val, auth_string[:al_auth.PUBLIC_KEY_CHARS_]]       # Return the public key without header and footer

