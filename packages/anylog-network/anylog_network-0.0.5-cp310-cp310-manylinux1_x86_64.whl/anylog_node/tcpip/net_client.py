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

# Echo client program
import socket
import sys
import threading
import time

import anylog_node.generic.utils_io as utils_io
import anylog_node.tcpip.message_header as message_header
import anylog_node.generic.process_log as process_log
import anylog_node.generic.params as params
import anylog_node.generic.utils_print as utils_print
import anylog_node.tcpip.net_utils as net_utils
import anylog_node.generic.utils_threads as utils_threads
import anylog_node.cmd.member_cmd as member_cmd


# run tcp client 10.0.0.124 2048 read aaa bbb

# =======================================================================================================================
# Change mode to UDP - this is called if UDP server is initiates
# =======================================================================================================================
def use_udp():
    global USE_UDP
    USE_UDP = True


# =======================================================================================================================
# Loop while data is read from file and send to dest server
# messages send include header + data
# =======================================================================================================================
def file_send(host: str, port: int, buff_size: int, input_file: str, output_file: str, flag: int, trace: int, consider_err:bool, auth_data:str):
    '''
    host - destination IP
    port - destination port
    buff_size - the size of the message buffer
    input_file - the name of the input file
    output_file - the name of the output file
    flag - determines the behaviour on the destination node. Flags are defined in message_header.py
    trace - the trace level
    consider_err - generate error message in case of a failure
    auth_data - signed IP:Port + Date-Time
    '''
    ret_val = True
    data_buffer = bytearray(buff_size)

    mem_view = memoryview(data_buffer)

    # set the destination IP and Port for outgoing messages
    if net_utils.set_ip_port_in_header(None, mem_view, host, port):
        return False

    message_header.set_generic_flag(mem_view, flag)  # this is a flag to the function called. For example, place file in watch dir

    output_file = output_file.replace(' ', '\t')  # Make a no space string when the message is read on the destination node

    if not output_file:
        # same file name as input file
        if flag:
            # flag determines where to place the file on dest machine - only extract file name
            file_name, file_type = utils_io.extract_name_type(input_file)
            if file_type:
                dest_file = file_name + '.' + file_type
            else:
                dest_file = file_name   # without flag - use the same name + path as the copied file
        else:
            dest_file = input_file
    else:
        dest_file = output_file


    offset_data = message_header.prep_command(mem_view, "file write " + dest_file)  # add the command size and info to the buffer

    # send a signed message with the IP, Port and Time that can be authenticated
    if not message_header.set_authentication(mem_view, auth_data):
        process_log.add("Error", "Internal Block Error - no space for authentication")
        return False

    if auth_data:
        # The first block includes the authentication string - the second data block can overwrite the string
        offset_in_buff = message_header.get_data_offset_after_authentication(mem_view)
    else:
        offset_in_buff = offset_data

    io_object = utils_io.IoHandle()  # object maintaing file handle and status

    if host == net_utils.get_external_ip():
        use_ip = net_utils.get_local_ip()   # Use the local IP to connect
    else:
        use_ip = host


    soc = socket_open(use_ip, port, "file write", 6, 3)

    if (utils_io.is_path_exists(input_file)):

        if soc:
            if io_object.open_file("read", input_file):

                if trace == 2:
                    counter = 0
                    data_copied = 0
                    utils_print.output("\ncounter   read      copied", True)

                block_number = 0
                last_block = False
                while 1:  # loop while file is read and transferred

                    block_number += 1

                    data_in = io_object.read_into_buffer(mem_view[offset_in_buff:])

                    if trace > 1:
                        counter += 1
                        data_copied += data_in
                        print_info = "\r\n-->[File Send] [Block #%u] [Bytes Copied: %u] [%s]" % (counter, data_copied, input_file)
                        utils_print.output(print_info, True)

                    message_header.incr_data_segment_size(mem_view, data_in)  # add length of data to message

                    if ((offset_in_buff + data_in) < buff_size):  # last message was send
                        last_block = True

                    message_header.set_block_number(mem_view, block_number,
                                                    last_block)  # place in the message header the block number and a flag representing last block to send

                    # if message_send(soc, data_buffer) == False:
                    if mem_view_send(soc, mem_view) == False:
                        break  # error sending the data

                    if last_block:
                        break

                    offset_in_buff = message_header.set_data_segment_to_command(mem_view)  # reset the size of the data in the block

                io_object.close_file()
            else:
                ret_val = False
        else:
            ret_val = False  # socket open failed
    else:  # input file does not exists
        ret_val = False
        error_msg = "Input file does not exists: " + input_file
        process_log.add("Error", error_msg)

    if soc:
        socket_close(soc)

    if not ret_val:
        if consider_err:
            member_cmd.output_echo_or_stdout(None, None, "File send failure from local node to: %s:%s" % (host,port ))

    return ret_val


# =======================================================================================================================
# Open socket - Try X times before return an error
# =======================================================================================================================
def socket_open(host: str, port: int, command:str, connect_timeout:int, retry_counter:int):

    '''
    connect_timeout - the wait time on the soc.connect((host, port) call - it is calculated by the user timeout value
    retry_counter - the number of times to call soc.connect((host, port) - it is calculated by the user timeout value
    '''
    ret_val = True

    trace_level = member_cmd.commands["run client"]['trace']

    try:

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        errno, value = sys.exc_info()[:2]
        err_msg = "TCP Client: Error socket create: {0} : {1}".format(str(errno), str(value))
        process_log.add("Error", err_msg)
        ret_val = False

    else:
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)  # setsockopt(level, optname, value)
        soc.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)  # alawys send the data
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 20 * params.TCP_BUFFER_SIZE)
        # soc.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 10))
        soc.setblocking(1)  # wait for the data to be send (equal to soc.settimeout(None)

        soc.settimeout(connect_timeout)

        counter = 0

        if trace_level > 2:
            utils_print.output("[Socket create] [Returned socket from: socket.socket(socket.AF_INET, socket.SOCK_STREAM)] %s" % str(soc), True)

        if net_utils.is_use_self(host, port):
            # If configuration defined: set self ip = dynamic
            # Change to the IP and Port set to self manage
            host, port = net_utils.get_self_ip_port()

        while ret_val:
            try:
                soc.connect((host, port))
            except:
                counter += 1
                errno, value = sys.exc_info()[:2]
                if retry_counter > 1 and counter == 1 and errno == socket.timeout:
                    continue  # try again once

                command_str = command.replace('\t', ' ')    # remove tabs from error msg

                if host == "0.0.0.0":
                    # This is a reply to a message that did not specified the reply ip and was not available on the socket
                    err_msg = "TCP Client Error: No destination IP for message: " + command_str
                    process_log.add_and_print("Error", err_msg)
                    soc = None
                    ret_val = False
                    break

                connection_refused = value.errno == 10061

                if not connection_refused and counter < retry_counter:
                    # in the case of all threads in the peer node are busy
                    err_msg = "TCP Client Error: #%u/%u Failed connection with %s:%u Error: (%s : %s) message: %s" % (
                    counter, retry_counter, host, port, str(errno), str(value), command_str)
                    process_log.add("Error", err_msg)
                    time.sleep(6)
                    continue

                if connection_refused:
                    err_msg = "TCP Client Error: Connection Refused : (%s : %s) - message not delivered: %s" % (host, port, command_str)
                else:
                    err_msg = "TCP Client Error: Connection with %s:%u failed with error: (%s : %s) - message not delivered: %s" % (host, port, str(errno), str(value), command_str)

                process_log.add("Error", err_msg)
                if soc:
                    socket_info = str(soc)
                else:
                    socket_info = "Socket Info not available"
                err_msg = "TCP Client Error: socket failed to connect: " + socket_info
                process_log.add("Error", err_msg)

                net_utils.test_ipaddr(host, port)  # place a message if the ip is in the wrong format
                soc = None
                ret_val = False
            break

    if trace_level > 2:
        utils_print.output("[Socket create] [Returned socket from: soc.connect((%s, %s))] %s" % (host, str(port), str(soc)), True)

    if ret_val:
        soc.settimeout(None)        #  If None is given -  the socket is put in blocking mode (for the send).

    # print_soc_process("open", soc)

    return soc


# =======================================================================================================================
# Close socket and place on the free list
#  use shutdown on a socket before you close it. The shutdown is an advisory to the socket at the other end. Depending on the argument you pass it.
# Details - https://docs.python.org/3/howto/sockets.html
# =======================================================================================================================
def socket_close(soc):
    # print_soc_process("close", soc)
    try:
        soc.shutdown()
    except:
        pass

    try:
        soc.close()
    except:
        pass


# =======================================================================================================================
# Prepare a message and send data to server
# The info in the message contains 2 parts: Command Part and Data part
# =======================================================================================================================
def message_prep_and_send(err_value, soc, mem_view: memoryview, command: str, auth_data: str, data: str,
                          info_type: int):
    message_header.set_error(mem_view, err_value)  # reset the error code
    message_header.set_info_type(mem_view, info_type)  # the type of info in the block
    message_header.prep_command(mem_view, command)  # add command to the send buffer

    data_encoded = data.encode()
    last_block = False
    block_number = 1
    bytes_transferred = 0

    # if use_authentication:
    if auth_data:
        # send a signed message with the IP, Port and Time that can be authenticated
        if not message_header.set_authentication(mem_view, auth_data):
            process_log.add("Error", "Internal Block Error - no space for authentication")
            return False

    while True:

        offset = message_header.insert_encoded_data(mem_view, data_encoded[bytes_transferred:])

        if not offset:
            last_block = True

        message_header.set_block_number(mem_view, block_number, last_block)

        ret_val = mem_view_send(soc, mem_view)  # Returns False if failed

        if not ret_val or last_block:
            break

        message_header.reset_authentication(mem_view)  # Authentication data is only needed with first message

        # send another block
        block_number += 1
        bytes_transferred += offset

    return ret_val


# =======================================================================================================================
# Send data to server
# =======================================================================================================================
def mem_view_send(soc, mem_view: memoryview):
    # print_soc_process("send", soc)

    file_no = soc.fileno()
    if file_no < 0:
        err_msg = "TCP Client failed to send a messgae, socket not active"
        process_log.add("Error", err_msg)
        utils_print.output(err_msg, True)
        return False

    thread_id = utils_threads.get_thread_number()
    message_header.set_send_socket_info(mem_view, 0, None, thread_id)

    ret_val = True
    try:
        soc.settimeout(10)  # 10 --> None
    except:
        errno, value = sys.exc_info()[:2]
        err_msg = "TCP Client failed to send a messgae, socket error: {0} : {1}".format(str(errno), str(value))
        process_log.add("Error", err_msg)
        utils_print.output(err_msg, True)
        return False

    if net_utils.get_TCP_debug():
        utils_print.output_box("TCP Client sending data using: %s" % str(soc))

    while 1:
        try:
            soc.sendall(mem_view)
            break
        except:
            errno, value = sys.exc_info()[:2]
            if errno == socket.timeout:
                err_msg = "TCP Client failed to send a message: timed out after 10 seconds"
                process_log.add("Error", err_msg)
                ret_val = False
                break  # replaced from break
            if value.args[0] == net_utils.BROKEN_PIPE:
                err_msg = "TCP Client failed to send a messgae: BROKEN PIPE"
            else:
                err_msg = "TCP Client failed to send a messgae: {0} : {1}".format(str(errno), str(value))
            process_log.add("Error", err_msg)
            utils_print.output(err_msg, True)
            ret_val = False
            break

    soc.settimeout(None)

    return ret_val
# -------------------------------------------------------------
# Print the current process
# -------------------------------------------------------------
def print_soc_process(process, soc):
    name = threading.current_thread().name.ljust(10)[:10]

    text = "\n%s :   %s    :    %s" % (name, process, str(soc))
    utils_print.output(text, False)
