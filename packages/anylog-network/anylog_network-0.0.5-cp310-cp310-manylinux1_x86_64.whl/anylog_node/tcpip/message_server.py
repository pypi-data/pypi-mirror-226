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

import socket
import sys
import time

import anylog_node.tcpip.net_utils as net_utils
import anylog_node.generic.utils_threads as utils_threads
import anylog_node.cmd.member_cmd as member_cmd
import anylog_node.generic.process_status as process_status
import anylog_node.generic.utils_print as utils_print
import anylog_node.generic.process_log as process_log
import anylog_node.tcpip.mqtt_client as mqtt_client
from anylog_node.generic.utils_columns import seconds_to_date
from anylog_node.blockchain.al_auth import validate_basic_auth

# The MQTT protocol: https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901041

MESSAGE_NOT_COMPLETE = 2001
END_SESSION = 2002

mqtt_topics_ = {}       # Topics registered pointing to the client ID (client_id as a f(topic))
counter_events_ = {}    #Global counter for event messages supporting the command - get messages
info_title_ = ["Protocol", "IP", "Event", "Success", "Last message time", "Error", "Last error time", "Error Code", "Details"]
workers_pool_ = None


class SESSION():
    def __init__(self, clientSoc, protocol_name, trace_level):

        self.clientSoc = clientSoc
        self.protocol_name = protocol_name
        self.trace_level = trace_level
        self.keep_alive = 60  # Default value for closing the session if no communication for so many seconds
        self.sessions_counter = 0
        self.msg_counter = 0  # Couner messages on this connection

        try:
            self.peer_ip = clientSoc.getpeername()[0]  # The IP of the peer node
        except:
            self.peer_ip = "Not determined"

        self.reset()
    # ----------------------------------------------------------------
    # The trace level is tested with every new message
    # ----------------------------------------------------------------
    def set_trace_level(self, trace_level):
        self.trace_level = trace_level

    # ----------------------------------------------------------------
    # The trace level is tested with every new message
    # ----------------------------------------------------------------
    def get_msg_counter(self):
        return self.msg_counter

    # ----------------------------------------------------------------
    # It is the maximum time interval in seconds that is permitted to elapse between the point at which the Client finishes
    # transmitting one Control Packet and the point it starts sending the next.
    # ----------------------------------------------------------------
    def get_keep_alive(self):
        return self.keep_alive


class MQTT_MESSAGES(SESSION):

    def reset(self):
        self.msg_type = -1
        self.msg_len = 0
        self.msg_size = 0
        self.msg_flags = 0
        self.fixed_hdr_len = 0  # Length of fixed header
        self.sessions_counter += 1  # number of times this session was called
        self.clean_session = 0
        self.will_flag = 0
        self.will_qos = 0
        self.will_retain = 0
        self.password_flag = 0
        self.user_name_flag = 0
        self.user_name = ""
        self.password = ""
        self.authenticated = False

        self.version = 0  # MQTT Version
        self.client_id = ""  # Each Client connecting to the Server has a unique ClientId
        self.will_topic = ""
        self.will_msg = None
        self.packet_identifier = 0xffffff  # A unique number provided by the sender in a publish message - will be set with 2 bytes value
        self.userdata = -1  # The value that is send to the mqtt client to idemtify how the topic was registered.
        self.payload = None  # Updated with the message data on a PUBLISH Message
        self.topic_name = None  # Updated with the topic name on a PUBLISH Message

    def get_seesion_id(self):
        # The Client Identifier is the session ID
        return self.client_id

    def get_msg_len(self):
        # Length as determined by the message header
        return self.msg_len
    # ----------------------------------------------------------------
    # Process one MQTT message
    # https://public.dhe.ibm.com/software/dw/webservices/ws-mqtt/mqtt-v3r1.html
    '''
    Reserved	0	Reserved
    CONNECT	1	Client request to connect to Server
    CONNACK	2	Connect Acknowledgment
    PUBLISH	3	Publish message
    PUBACK	4	Publish Acknowledgment
    PUBREC	5	Publish Received (assured delivery part 1)
    PUBREL	6	Publish Release (assured delivery part 2)
    PUBCOMP	7	Publish Complete (assured delivery part 3)
    SUBSCRIBE	8	Client Subscribe request
    SUBACK	9	Subscribe Acknowledgment
    UNSUBSCRIBE	10	Client Unsubscribe request
    UNSUBACK	11	Unsubscribe Acknowledgment
    PINGREQ	12	PING Request
    PINGRESP	13	PING Response
    DISCONNECT	14	Client is Disconnecting
    Reserved	15	Reserved
    '''
    # ----------------------------------------------------------------
    def processs_msg(self, status, mem_view, length):


        remaining_length = length                 # The amount of data left in the buffer to process

        while True:

            if remaining_length < 3:
                ret_val = MESSAGE_NOT_COMPLETE
                break                            # The minimum is 3 bytes - (type + size + message)

            ret_val = self.process_fixed_header(mem_view, remaining_length)
            if ret_val:
                break

            self.msg_counter += 1

            # Could be multiple messages on the mem_view buffer
            multiple_messages = remaining_length > self.msg_len  # Test if the size of the data received is larger than the message size

            if self.msg_type == 1:
                # connect
                if self.msg_counter != 1:
                    # The Server MUST process a second CONNECT Packet sent from a Client as a protocol violation and disconnect the Client [MQTT-3.1.0-2].
                    ret_val = END_SESSION
                else:
                    ret_val = self.connect_msg( status, mem_view, multiple_messages )
                    count_event("MQTT", self.peer_ip, "CONNECT", ret_val, "")
            elif self.msg_type == 3:
                # Message   - MQTT Control Packet type (3)
                ret_val = self.publish_msg( mem_view )

                if ret_val == process_status.Unrecognized_mqtt_topic:
                    details = self.topic_name
                else:
                    details = ""
                count_event("MQTT", self.peer_ip, "PUBLISH", ret_val, details)

            elif self.msg_type == 6:
                # A PUBREL Packet is the response to a PUBREC Packet. It is the third packet of the QoS 2 protocol exchange.
                ret_val = self.pubrel_msg( mem_view )
            elif self.msg_type == 8:
                # Register to a topic
                ret_val = self.subscribe_msg( mem_view )
            elif self.msg_type == 10:
                # An UNSUBSCRIBE message is sent by the client to the server to unsubscribe from named topics.
                # Needs to return Unsubscribe acknowledgment (UNSUBACK)
                ret_val = self.unsubscribe_mqtt( mem_view )

            elif self.msg_type == 12:
                # Request that the Server responds to confirm that it is alive
                ret_val = self.ping_msg()
            else:
                err_msg = "Non supported MQTT message type %u" % self.msg_type
                utils_print.output_box(err_msg)
                ret_val = END_SESSION
                break
            if ret_val:
                remaining_length = 0
                break

            if multiple_messages:
                remaining_length = self.shift_data( mem_view, remaining_length)  # Set next message to processing
            else:
                remaining_length = 0
                break                           # No more messages in mem_view

        return [ret_val, remaining_length]

    # ----------------------------------------------------------------
    # Shift the next message to beginning of the buffer and return the remaining lenth
    # ----------------------------------------------------------------
    def shift_data( self, mem_view, remaining_length):

        next_message_length = remaining_length - self.msg_len
        mem_view[:next_message_length] = mem_view[self.msg_len: self.msg_len + next_message_length]

        return next_message_length

    # ----------------------------------------------------------------
    # Process Fixed Header
    # ----------------------------------------------------------------
    def process_fixed_header(self, mem_view, remaining_length):

        self.msg_type = mem_view[0] >> 4  # 1st 4 bits - MQTT Control Packet types
        self.msg_flags = mem_view[0] & 7  # low 4 bits -  Flags specific to each MQTT Control Packet types

        message_size, bytes_used = msg_get_var_int(mem_view, 1) # (section 3.1.1) length of the Variable Header plus the length of the Payload
        self.fixed_hdr_len = 1 + bytes_used
        self.msg_len = ( message_size + self.fixed_hdr_len)        # Add the length of the FIXED HEADER

        if self.msg_len > remaining_length:         # remaining_length is the data in the buffer
            ret_val = MESSAGE_NOT_COMPLETE             # get more data
        else:
            ret_val = process_status.SUCCESS
        return ret_val


    # ----------------------------------------------------------------
    # Process PINGREQ  - Request that the Server responds to confirm that it is alive
    # ----------------------------------------------------------------
    def ping_msg(self):

        # The server needs to respond with PINGRESP
        list_response = [0xd0, 0x0,  # Fixed header with PINGRESP
                    ]

        msg_response = bytearray(list_response)
        ret_val = send_msg("MQTT", self.clientSoc, msg_response)
        return ret_val

    # ----------------------------------------------------------------
    # Process SUBSCRIBE - Subscribe to topics
    # ----------------------------------------------------------------
    def subscribe_msg(self, mem_view):

        ret_val = process_status.SUCCESS
        # Fixed header - 2 bytes
        remaining_length, bytes_used = msg_get_var_int(mem_view, 1) # This is the length of Variable Header plus the length of the Payload
        message_length = remaining_length + bytes_used + 1          # length of Header + var Header + Payload

        offset = 1 + bytes_used     # Offset to Var Header
        packet_identifier = msg_get_int(mem_view, offset, 2)
        if not packet_identifier:
            ret_val = process_status.Err_in_broker_msg_format
        else:
            offset += 2         # Offset to Payload

            reply_var_header = [0,0]        # Placeholder for the Packet Identifier

            while offset < message_length:
                topic_length = msg_get_int(mem_view, offset, 2)
                if not topic_length:
                    ret_val = process_status.Err_in_broker_msg_format
                    break
                topic_name = msg_get_bytes(mem_view, offset + 2, topic_length)
                if not topic_name:
                    ret_val = process_status.Err_in_broker_msg_format
                    break
                offset += (2 + topic_length)
                qos = mem_view[offset]

                reply_var_header.append(qos)        # need to return the QoS for every Topic

                offset += 1

                if self.trace_level:
                    message = "\r\nSubscribe to topic: [%s]" % (topic_name)
                    utils_print.output(message, True)

        if not ret_val:
            # reply with SUBACK

            list_ack = [   0x90,    ]            # Fixed header ( SUBACK )

            counter = len(reply_var_header)     # Number of topics
            if counter >= 128:
                # 2 bytes for the length for the length of var header + payload
                low_bits = counter & 0x7f
                low_bits |= 0x80
                high_bits = counter >> 7
                list_ack.append(low_bits)
                list_ack.append(high_bits)
            else:
                # One byte for the length of var header + payload
                list_ack.append(counter)

            list_ack += reply_var_header

            msg_ack = bytearray(list_ack)
            msg_ack[2:4] = packet_identifier.to_bytes(2, byteorder='big', signed=False)  # set packet identifier

            ret_val = send_msg("MQTT", self.clientSoc, msg_ack)     # send reply message

        return ret_val

    # ----------------------------------------------------------------
    # Process CONNECT MESSAGE
    # send acknowledgement to the client
    # Details at https://docs.solace.com/MQTT-311-Prtl-Conformance-Spec/MQTT%20Control%20Packets.htm
    # The Server MUST acknowledge the CONNECT packet with a CONNACK packet containing a 1075 0x00 (Success) Reason Code [MQTT-3.1.4-5].
    # ----------------------------------------------------------------
    def connect_msg(self, status, mem_view,  multiple_messages):

        offset_version = self.fixed_hdr_len + 6     # 2 bytes protocol name length + len("MQTT")
        self.version = mem_view[offset_version]

        offset_connect = offset_version + 1
        connect_flags = mem_view[offset_connect]

        # If CleanSession is set to 0, the Server MUST resume communications with the Client
        # based on state from the current Session (as identified by the Client identifier).
        # If there is no Session associated with the Client identifier the Server MUST create a new Session.
        # The Client and Server MUST store the Session after the Client and Server are disconnected [MQTT-3.1.2-4].
        # After the disconnection of a Session that had CleanSession set to 0,
        # the Server MUST store further QoS 1 and QoS 2 messages that match any subscriptions that the client
        # had at the time of disconnection as part of the Session state.
        # If CleanSession is set to 1, the Client and Server MUST discard any previous Session and start a new one.
        # This Session lasts as long as the Network Connection. State data associated with this Session MUST NOT be reused in any subsequent Session
        self.clean_session = (connect_flags & 0x2) >> 1

        # Keep the last message and last QoS in case there is disconnect.
        # When the bit of Will Flag is 1, Will QoS and Will Retain will be read. At this time,
        # the specific contents of Will Topic and Will Message will appear in the message body,
        # otherwise the Will QoS and Will Retain will be ignored.
        # When the Will Flag bit is 0, Will Qos and Will Retain are invalid.
        self.will_flag =  (connect_flags & 0x4) >> 2

        #  2 bits specify the QoS level to be used when publishing the Will Message
        self.will_qos = (connect_flags & 0x18) >> 3

        # If Will Retain is set to 0, the Server MUST publish the Will Message as a non-retained message [MQTT-3.1.2-16].
        # If Will Retain is set to 1, the Server MUST publish the Will Message as a retained message
        self.will_retain = (connect_flags & 0x20) >> 5

        self.password_flag = (connect_flags & 0x40) >> 6
        self.user_name_flag = (connect_flags & 0x80) >> 7

        # It is the maximum time interval in seconds that is permitted to elapse between the point at which the Client finishes
        # transmitting one Control Packet and the point it starts sending the next.
        self.keep_alive = msg_get_int(mem_view, offset_connect + 1, 2)

        offset = offset_connect + 3         # offset payload

        # Each Client connecting to the Server has a unique ClientId
        client_id_length = msg_get_int(mem_view, offset, 2)
        self.client_id = msg_get_bytes(mem_view, offset + 2, client_id_length)
        offset += (client_id_length + 2)

        if self.will_flag:
            will_topic_length = msg_get_int(mem_view, offset, 2)
            self.will_topic = msg_get_bytes(mem_view, offset + 2, will_topic_length)
            offset += (will_topic_length + 2)

            will_msg_length = msg_get_int(mem_view, offset, 2)
            self.will_msg = mem_view[offset + 2: offset + 2 + will_msg_length]
            offset += (will_msg_length + 2)

        if self.user_name_flag:
            name_length = msg_get_int(mem_view, offset, 2)
            user_name = msg_get_bytes(mem_view, offset + 2, name_length)
            offset += (name_length + 2)
        else:
            user_name = ""

        if self.password_flag:
            password_length = msg_get_int(mem_view, offset, 2)
            password = msg_get_bytes(mem_view, offset + 2, password_length)
            offset +=2
        else:
            password = ""

        ret_val = self.register_user(status, user_name, password)  # with a new user - authenticate the user
        if not ret_val:

            if self.trace_level:
                message = "\r\nConnect from user: [%s]" % (self.user_name)
                utils_print.output(message, True)


            list_ack = [   0x20,        0x2,                # Fixed header ( CONNACK - 1119)
                        # Variable Header - Section 3.1.2
                           0x00,            # Byte 1 / 1132 is the "Connect Acknowledge Flags : 0 for new session
                           0x00,            # Byte 2 / 1165 Connect return Code : 0 for Connection Accepted
                       ]

            msg_ack = bytearray(list_ack)

            if multiple_messages:
                # No need to acknowledge if received multiple messages on the buffer
                ret_val = process_status.SUCCESS
            else:
                # Callback for MQTT is explained here - http://www.steves-internet-guide.com/mqtt-python-callbacks/
                ret_val = send_msg("MQTT", self.clientSoc, msg_ack)

        return ret_val
    # ----------------------------------------------------------------
    # Process Publish MESSAGE
    # https://openlabpro.com/guide/mqtt-packet-format/
    '''
    The process for QoS 2
    1. A receiver gets a QoS 2 PUBLISH packet from a sender
    2 -The receiver sends a PUBREC message 
    3. If the sender doesn’t receive an acknowledgement (PUBREC)  it will resend the message with the DUP flag set.
    4. When the sender receives an acknowledgement message PUBREC it then sends a message release message (PUBREL). The message can be deleted from the queue.
    5. If the receiver doesn’t receive the PUBREL it will resend the PUBREC message
    5. When the receiver receives the PUBREL message it can now forward the message onto any subscribers.
    6. The receiver then send a publish complete (PUBCOMP) .
    7. If the sender doesn’t receive the PUBCOMP message it will resend the PUBREL message.
    8. When the sender receives the PUBCOMP the process is complete and it can delete the message from the outbound queue, and also the message state.
    '''
    # ----------------------------------------------------------------
    def publish_msg(self, mem_view):

        global mqtt_topics_

        ret_val = process_status.SUCCESS

        # Section 3.3.1 PUBLISH Fixed Header

        dup_flag = mem_view[0] & 8      # If the bit is on = re-delivery of the message
        qos_level = (mem_view[0] & 6) >> 1   # 2 bits for QoS
        retain_flag = mem_view[0] & 1   # Keep the last data published

        # Section 3.3.2 PUBLISH Variable Header
        # The Variable Header of the PUBLISH Packet contains the following fields in the order: Topic Name,
        # Packet Identifier, and Properties. The rules for encoding Properties are described in section 2.2.2.

        offset_var_header = self.fixed_hdr_len
        topic_name_length = msg_get_int(mem_view, offset_var_header, 2)
        self.topic_name = msg_get_bytes( mem_view, offset_var_header + 2, topic_name_length)

        offset_var_header += (2 + topic_name_length)

        new_message = True
        if qos_level:
            # If QoS > 0 --> reply to sender
            in_identifier =  msg_get_int(mem_view, offset_var_header, 2)    # Section 2.2.1 Packet Identifier
            offset_var_header += 2
            if dup_flag and in_identifier == self.packet_identifier:
                # The same message delivered again
                new_message = False       # repeat of a message that was received
            else:
                self.packet_identifier = in_identifier  # new message

        if new_message:  # not a message repeat

            offset_payload = offset_var_header
            length_payload = self.msg_len - offset_payload

            self.payload = msg_get_bytes(mem_view, offset_payload, length_payload)
            if not self.payload:
                ret_val = process_status.Err_in_broker_msg_format

            if self.topic_name in mqtt_topics_: # there is a subscription to the topic
                # The topic name was registered on the local broker
                # Move the published data to the streamer through the MQTT Client on_message process
                self.userdata = mqtt_topics_[self.topic_name]
            else:
                self.userdata = 0
                ret_val = process_status.Unrecognized_mqtt_topic
        if not ret_val:
            # Respond to the PUBLISH packet:
            # If QoS is 0 - None
            # If QoS is 1 - PUBACK Packet   --> Publish Acknowledgement
            # If QoS is 2 - PUBREC Packet   --> Publish Received
            if not qos_level:
                if self.userdata:   # if self.userdata is 0 --> no subscription to the topic
                    ret_val = mqtt_client.process_message(self.topic_name, self.userdata, self.payload)
            elif self.packet_identifier <= 0xffff:
                if qos_level == 1:
                    # Publish Acknowledgement First
                    ret_val = self.send_puback()
                    if not ret_val:
                        if self.userdata:  # if self.userdata is 0 --> no subscription to the topic
                            ret_val = mqtt_client.process_message(self.topic_name, self.userdata, self.payload)
                elif qos_level == 2:
                    # Publish after PUBREL message from the sender of the data
                    ret_val = self.send_pubrec()

        if self.trace_level:
            if not new_message:
                msg_status = "Repeat of processed msg: PUBLISH"
            else:
                msg_status = "Publish a new msg: PUBLISH"

            if not self.userdata:   # if self.userdata is 0 --> no subscription to the topic
                msg_result = "Non subscribed topic"
            else:
                msg_result = "With subscription"
            if ret_val < 2000:
                err_msg = process_status.get_status_text(ret_val)
            else:
                err_msg = str(ret_val)

            trace_msg = "\r\n[MQTT] [%s] [Topic: %s] [QoS: %u] [--> %s] [--> %s] [payload: %s] " % (msg_status, self.topic_name, qos_level, msg_result, err_msg, self.payload)

            utils_print.output(trace_msg, True)

        return ret_val

    # ----------------------------------------------------------------
    # A PUBREL Packet is the response to a PUBREC Packet.
    #
    #  With this packet - forward the message onto any subscribers.
    #
    # It is the third packet of the QoS 2 protocol exchange.
    # http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718043
    # ----------------------------------------------------------------
    def pubrel_msg(self, mem_view):
        # Fixed header - 2 bytes
        remaining_length, bytes_used = msg_get_var_int(mem_view, 1) # This is the length of Variable Header plus the length of the Payload

        purel_identifier = msg_get_int(mem_view, bytes_used + 1, 2)

        if purel_identifier == self.packet_identifier:
            # Got confirmatiom for the PUBREL Packet
            if self.userdata:  # if self.userdata is 0 --> no subscription to the topic
                ret_val = mqtt_client.process_message(self.topic_name, self.userdata, self.payload)  # Transfer data to MQTT Client
                if not ret_val:
                    ret_val = self.send_pubcomp()   # the PUBCOMP Packet is the response to a PUBREL Packet. It is the fourth and final packet of the QoS 2 protocol exchange.
        else:
            ret_val = process_status.SUCCESS        # Ignore the message
            if self.trace_level:
                message = "\r\n[MQTT] [Publish] [QoS 2] [Packet confirmation returned wrong value]"
                utils_print.output(message, True)

        return ret_val
    # ----------------------------------------------------------------
    # the PUBCOMP Packet is the response to a PUBREL Packet.
    # It is the fourth and final packet of the QoS 2 protocol exchange.
    # ----------------------------------------------------------------
    def send_pubcomp(self):
        list_pubcomp = [0x70, 0x2,  # Fixed header ( PUBACK )
                    # Variable Header
                    0x00,
                    0x00,
                    ]

        list_pubcomp[2] = self.packet_identifier >> 8
        list_pubcomp[3] = self.packet_identifier & 0xff

        msg_pubcomp = bytearray(list_pubcomp)
        ret_val = send_msg("MQTT", self.clientSoc, msg_pubcomp)
        return ret_val

    # ----------------------------------------------------------------
    # A PUBREC Packet is the response to a PUBLISH Packet with QoS 2.
    # It is the second packet of the QoS 2 protocol exchange.
    # ----------------------------------------------------------------
    def send_pubrec(self):

        list_pubrec = [0x50, 0x2,  # Fixed header ( PUBACK )
                    # Variable Header
                    0x00,
                    0x00,
                    ]

        list_pubrec[2] = self.packet_identifier >> 8
        list_pubrec[3] = self.packet_identifier & 0xff

        msg_pubrec = bytearray(list_pubrec)
        ret_val = send_msg("MQTT", self.clientSoc, msg_pubrec)
        return ret_val

    # ----------------------------------------------------------------
    # A PUBACK Packet is the response to a PUBLISH Packet with QoS level 1.
    # ----------------------------------------------------------------
    def send_puback(self):

        list_puback = [0x50, 0x2,  # Fixed header ( PUBACK )
                    # Variable Header
                    0x00,
                    0x00,
                    ]

        list_puback[2] = self.packet_identifier >> 8
        list_puback[3] = self.packet_identifier & 0xff


        msg_puback = bytearray(list_puback)
        ret_val = send_msg("MQTT", self.clientSoc, msg_puback)
        return ret_val
    # ----------------------------------------------------------------
    # Validate user with basic authentication
    # with a new user - authenticate the user
    # ----------------------------------------------------------------
    def register_user(self, status, user_name, password):

        if user_name == self.user_name and password == self.password and self.authenticated:
            ret_val = process_status.SUCCESS       # Same user as before and was authenticated
        else:
            if not validate_basic_auth(status, user_name, password):
                ret_val = process_status.Failed_message_authentication
            else:
                # Authenticated
                self.user_name = user_name
                self.password = password
                self.authenticated = True
                ret_val = process_status.SUCCESS
        return ret_val

    # ----------------------------------------------------------------
    # An UNSUBSCRIBE message is sent by the client to the server to unsubscribe from named topics.
    # UNSUBSCRIBE messages use QoS level 1 to acknowledge multiple unsubscribe requests. The corresponding UNSUBACK message
    # is identified by the Message ID. Retries are handled in the same way as PUBLISH messages.
    # Details in section 3.10 - https://public.dhe.ibm.com/software/dw/webservices/ws-mqtt/mqtt-v3r1.html#unsubscribe
    # ----------------------------------------------------------------
    def unsubscribe_mqtt(self, mem_view):

        unsuback = [0x0b, 0x0,  # Fixed header ( UNSUBACK  - 1100)
                    # Variable Header - Section 3.1.2
                    0x00,  # 0
                    0x02,  # Remaining length (2)
                    0x00,  # 	Message ID MSB (0)
                    0x10   #    Message ID LSB (10)
                    ]

        msg_ack = bytearray(unsuback)


        # Callback for MQTT is explained here - http://www.steves-internet-guide.com/mqtt-python-callbacks/
        ret_val = send_msg("MQTT", self.clientSoc, msg_ack)

        return ret_val


sessions_types = {
    "MQTT"  : MQTT_MESSAGES
}
# ----------------------------------------------------------------
# Init mqtt server
# The server protocol - https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.pdf
# Edgex setup - https://github.com/oshadmon/Udemy/blob/master/EdgeX/Lab_Setup.md
# Examole python HBMQTT https://hbmqtt.readthedocs.io/en/latest/
# ----------------------------------------------------------------
def message_broker( host: str, port: int, is_bind:bool, workers_count, trace ):
    global workers_pool_

    # Set a pool of workers threads
    workers_pool_ = utils_threads.WorkersPool("Message", workers_count)

    net_utils.message_server("Message Broker", "broker", host, port, 2048, workers_pool_, rceive_data, is_bind, trace)

    net_utils.remove_connection(2)

    workers_pool_ = None

# ----------------------------------------------------------------------------------
# Determine the protocol to use
# ----------------------------------------------------------------------------------
def get_protocol(mem_view, msg_length):
    # Identify the protocol to use

    if msg_length < 8:
        return "not_complete"       # MQTT protocol requires 8 bytes

    if is_mqtt(mem_view):
        return "MQTT"

    return "UNKNOWN"

# ----------------------------------------------------------------------------------
# Determine the protocol to use
# ----------------------------------------------------------------------------------
def is_mqtt(mem_view):

    ret_val = False
    protocol_name_length = msg_get_int(mem_view, 2, 2)
    if protocol_name_length < 20:
        protocol_name = msg_get_bytes(mem_view, 4, protocol_name_length).lower()
        if not protocol_name:
            ret_val = process_status.Err_in_broker_msg_format
        elif protocol_name == "mqtt" or "'mqisdp'":
            # In MQTT 3.1 the protocol name is "MQISDP". In MQTT 3.1.1 the protocol name is represented as "MQTT".
            # https://www.oasis-open.org/committees/download.php/55095/mqtt-diffs-v1.0-wd01.doc
            ret_val = True

    return ret_val


# ----------------------------------------------------------------------------------
# Get bytes from mqtt message buffer
# ----------------------------------------------------------------------------------
def msg_get_bytes(msg_buff, offset, length):

    try:
        ret_bytes = bytes(msg_buff[offset:offset + length]).decode()
    except:
        errno, value = sys.exc_info()[:2]

        err_msg = "Failed to decode message withe error: %s : %s".format(str(errno), str(value))

        process_log.add("Error", err_msg)

        ret_bytes = None

    return ret_bytes
# ----------------------------------------------------------------------------------
# Get int from mqtt message buffer
# ----------------------------------------------------------------------------------
def msg_get_int(msg_buff, offset, length):

    try:
        int_value = int.from_bytes(msg_buff[offset: offset + length], byteorder='big', signed=False)
    except:
        errno, value = sys.exc_info()[:2]

        err_msg = "Failed to decode message withe error: %s : %s".format(str(errno), str(value))

        process_log.add("Error", err_msg)

        int_value = None
    return int_value


# ----------------------------------------------------------------------------------
# Get variable int from mqtt message buffer
# Explained in section 1.5.5 ( Line 268 )
#The Variable Byte Integer is encoded using an encoding scheme which uses a single byte for values up 299 to 127.
# Larger values are handled as follows:
# The least significant seven bits of each byte encode the data,
# and the most significant bit is used to indicate whether there are bytes following in the representation.
# ----------------------------------------------------------------------------------
def msg_get_var_int(msg_buff, offset):

    # else:
    multiplier = 1
    value = 0
    for i in range (4):          # up to 3 bytes
        encodedByte = msg_buff[offset + i]
        value += (encodedByte & 127) * multiplier
        if encodedByte <= 127:
            break
        multiplier *= 128

    return [value, i + 1]       # return value and size

# ----------------------------------------------------------------------------------
# send message to the client
# ----------------------------------------------------------------------------------
def send_msg(server_type, clientSoc, message_data):

    while 1:
        try:
            clientSoc.sendall(message_data)
        except:
            errno, value = sys.exc_info()[:2]
            err_msg = "{0} Server failed to send a messgae: {1} : {2}".format(server_type, str(errno), str(value))
            process_log.add("Error", err_msg)
            ret_val = process_status.MQTT_server_error
            break
        else:
            ret_val = process_status.SUCCESS
            break

    return ret_val

# ----------------------------------------------------------------------------------
# Log the message info
# ----------------------------------------------------------------------------------
def log_msg(mem_view):

    message_type = mem_view[0] >> 4  # 1st 4 bits - MQTT Control Packet types
    message_flags = mem_view[0] & 7  # low 4 bits -  Flags specific to each MQTT Control Packet types

    remaining_length, var_int_length = msg_get_var_int(mem_view, 1)  # Section 2.1.4 ( Line 416 )
    packet_length = remaining_length + 1  # 1 byte for  the message type (4 bits) and message flags (4 bits)
    packet_length += var_int_length  # size of the var int

    protocol_name_length = msg_get_int(mem_view, var_int_length + 1, 2)
    if protocol_name_length:
        protocol_name = msg_get_bytes(mem_view, var_int_length + 3, protocol_name_length)
        if protocol_name:
            char_str = ""
            for x in range (packet_length):
                byte_val = mem_view[x]
                if byte_val >= 0x20:
                    char_str += chr(byte_val)
                else:
                    char_str += '[%u:0x%s]' % (x,str(byte_val))

            log_buff = "\r\nMQTT: Type: %u Flags: %u length: %u  Protocol: %s String: %s" % (message_type, message_flags, packet_length, protocol_name, char_str)

            utils_print.output(log_buff, True)

# ----------------------------------------------------------------
# Register MQTT Topics when broker is "local"
# Command example:
# run mqtt client where broker = local and ...
# ----------------------------------------------------------------
def subscribe_mqtt_topics(status, client_id):

    global mqtt_topics_

    # Get the topics associated with this client id
    topics_dict = mqtt_client.get_topics_by_id( client_id )

    if not topics_dict:
        status.add_error("Message Broker Error: MQTT process: No topics associated with client id %u" % client_id)
        ret_val = process_status.ERR_process_failure
    else:
        ret_val = process_status.SUCCESS
        for topic in topics_dict:
            mqtt_topics_[topic] = client_id

    return ret_val
# ----------------------------------------------------------------
# unregister MQTT Topics when broker is "local"
# When "exit mqtt" is called
# ----------------------------------------------------------------
def unsubscribe_mqtt_topics(status, client_id):
    global mqtt_topics_

    # Get the topics associated with this client id
    topics_dict = mqtt_client.get_topics_by_id(client_id)

    if not topics_dict:
        status.add_error("Message Broker Error: MQTT process: No topics associated with client id %u" % client_id)
        ret_val = process_status.ERR_process_failure
    else:
        ret_val = process_status.SUCCESS
        for topic in topics_dict:
            if topic in mqtt_topics_ and mqtt_topics_[topic] == client_id:
                del mqtt_topics_[topic]

    return ret_val
# ----------------------------------------------------------------
# Count message events to support AnyLog command - "get messages"
# ----------------------------------------------------------------
def count_event(msg_protocol, msg_ip, msg_event_name, ret_code, details):
    global counter_events_  # protocol --> client --> event name --> success counter --> date --> error counter  --> date --> error_code

    # Get or set the protocol entry
    if msg_protocol not in counter_events_:
        protocol = {}
        counter_events_[msg_protocol] = protocol
    else:
        protocol = counter_events_[msg_protocol]

    # Get or set the IP entry
    if msg_ip not in protocol:
        ip = {}
        protocol[msg_ip] = ip
    else:
        ip = protocol[msg_ip]

    # Get or set the event name entry
    if msg_event_name not in ip:
        info_stat = [0,0,0,0,0,""]        # success counter --> date --> error counter  --> date --> error_code --> details
        ip[msg_event_name] = info_stat
    else:
        info_stat = ip[msg_event_name]

    # Update the info
    if ret_code:
        info_stat[2] += 1   # Error
        info_stat[3] = int(time.time())
        info_stat[4] = ret_code
        info_stat[5] = details
    else:
        info_stat[0] += 1   # Success
        info_stat[1] = int(time.time())

# ----------------------------------------------------------------
# Get info to support AnyLog command - "get messages"
# ----------------------------------------------------------------
def show_info():

    global counter_events_  # protocol --> client --> event name --> success counter --> date --> error counter  --> date --> error_code
    global info_title_

    info_table = []
    for protocol, protocol_info in counter_events_.items():
        for ip, ip_info in protocol_info.items():
            for event_name, event_info in ip_info.items():
                if event_info[1]:
                    success_date = seconds_to_date(event_info[1], "%Y-%m-%d %H:%M:%S")
                else:
                    success_date = ""
                if event_info[3]:
                    error_date = seconds_to_date(event_info[3], "%Y-%m-%d %H:%M:%S")
                else:
                    error_date = ""

                error_code = event_info[4]
                if not error_code:
                    err_msg = ""
                elif error_code < 2000:
                    err_msg = process_status.get_status_text(event_info[4])
                else:
                    err_msg = str(error_code)
                counter_success = format(event_info[0], ",")
                counter_error = format(event_info[2], ",")
                details = event_info[5]
                info_table.append([protocol, ip, event_name, counter_success, success_date, counter_error, error_date, err_msg, details])

    reply = utils_print.output_nested_lists(info_table, "Message Broker Stat", info_title_, True)
    return reply

# ------------------------------------------------------------------
# Return info on the TCP Server in command - show processes
# ------------------------------------------------------------------
def get_info():
    global workers_pool_

    info_str = net_utils.get_connection_info(2)
    if workers_pool_:
        info_str += ", Threads Pool: %u" %  workers_pool_.get_number_of_threds()

    return info_str

# ----------------------------------------------------------------
# Receive data and process
# MQTT Example is here - http://www.steves-internet-guide.com/publishing-messages-mqtt-client/
# Echo Server:  https://realpython.com/python-sockets/
# https://github.com/eclipse/paho.mqtt.python/blob/master/tests/testsupport/broker.py
# ----------------------------------------------------------------
def rceive_data(status, mem_view, params, clientSoc, ip_in, port_in, thread_buff_size):

    #clientSoc.setblocking(1)  # wait for the data to be received (equal to soc.settimeout(None)

    clientSoc.settimeout(10)

    ret_val = process_status.SUCCESS
    msg_size = 0

    known_protocol = False
    session = None        # AN object created once the protocol is identified
    counter = 0

    data_buffer = mem_view
    data_buff_size = thread_buff_size

    while True:

        counter += 1

        trace_level = member_cmd.commands["run message broker"]['trace']

        if known_protocol:
            session.set_trace_level(trace_level)

        if ret_val == MESSAGE_NOT_COMPLETE:
            # This is not the first loop to get the message
            # Not all the data of the message is in the buffer
            if session.get_msg_len() > data_buff_size:
                # Need to increase the buffer size to contain the message
                data_buff_size = session.get_msg_len()
                new_buffer = memoryview(bytearray(data_buff_size))
                new_buffer[:msg_size] = data_buffer[:msg_size]  # Copy the message prefix to the new buffer
                data_buffer = new_buffer

        try:
            #length = clientSoc.recv_into(data_buffer[msg_size:], data_buff_size - msg_size)
            # The send is in client.py line # 2335
            # In client.py - place breakpoints on line 664 (self._sock_recv) and line 667 (self._sock.send)
            length, address = clientSoc.recvfrom_into(data_buffer[msg_size:], data_buff_size - msg_size)

        except:
            if not net_utils.is_active_connection(2) or process_status.is_exit("broker", False):
                # is_active_connection is tested as "exit broker" may have reset the exit flag
                ret_val = process_status.SUCCESS
                break           # The main broker thread exited or all terminated

            errno, value = sys.exc_info()[:2]
            if errno == socket.timeout:
                ret_val = process_status.SUCCESS

                if not known_protocol:
                    if counter < 4:
                        continue        # wait more time before closing the socket
                    break              # No message showed up

                if not session or (message_time + session.get_keep_alive()) < int(time.time()):
                    break       # If no messages arrived for 50 seconds (default) --> close connections
                continue


            err_msg = "Message Broker disconnected from: %s with error: %s" % (str(clientSoc), str(value))
            process_log.add("Error", err_msg)
            ret_val = process_status.ERR_network
            break
        else:
            if trace_level > 1:
                utils_print.output_box("Message Broker received %u bytes from: %s" % (length, str(clientSoc)))

            if not length:
                ret_val = process_status.SUCCESS
                break

            #if len == 2048:
                #continue

            if not net_utils.is_active_connection(2) or process_status.is_exit("broker", False):
                # is_active_connection is tested as "exit broker" may have reset the exit flag
                ret_val = process_status.SUCCESS
                break           # The main broker thread exited or all terminated


            message_time = int(time.time())         # Get the time of the message received

            msg_size += length
            if msg_size < 3:
                continue                            # The minimum is 3 bytes - (type + size + message)
            if not known_protocol:
                # First call with this connection
                protocol_name = get_protocol(data_buffer, msg_size)
                if protocol_name == "UNKNOWN":
                    break           # Non recognized protocol
                if protocol_name == "not_complete":
                    continue        # Need more data
                known_protocol = True
                if session:
                    session.reset()
                else:
                    session = sessions_types[protocol_name](clientSoc, protocol_name, trace_level)

            # process the protocol
            ret_val, msg_size = session.processs_msg(status, data_buffer, msg_size)

            if ret_val == END_SESSION:
                break

            if ret_val == MESSAGE_NOT_COMPLETE:
                continue        # Not all the data of the message is available

    if trace_level:
        utils_print.output_box("Message Broker thread completed process using: %s" % (str(clientSoc)))

    return ret_val

# ------------------------------------------------------------------
# Return info on the workers pool
# returns info when calling - get msg pool
# ------------------------------------------------------------------
def get_threads_obj():

    global workers_pool_
    return workers_pool_


