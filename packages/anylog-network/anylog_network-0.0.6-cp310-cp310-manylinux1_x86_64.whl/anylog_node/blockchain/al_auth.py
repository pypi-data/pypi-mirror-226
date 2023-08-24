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

# Storing passwords using keyring - https://pypi.org/project/keyring/#description
# pip install keyring
# May require install of dbus-python


# https://cryptography.io/en/latest/

try:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
    from cryptography.fernet import \
        Fernet  # Example is here - https://www.geeksforgeeks.org/create-a-credential-file-using-python/

    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except:
    use_node_authentication_ = False
    crypto_installed_ = False
else:
    use_node_authentication_ = True
    crypto_installed_ = True

use_user_authentication_ = False

use_encryption_ = False

import sys
import os
import subprocess
import uuid
import binascii
import base64
from datetime import datetime, timedelta
import secrets

import anylog_node.generic.params as params
import anylog_node.generic.process_status as process_status
import anylog_node.generic.utils_io as utils_io
from anylog_node.generic.utils_json import str_to_json, to_string, test_key_value, str_to_list
from anylog_node.generic.utils_columns import get_current_time_in_sec, get_date_time_from_utc_sec
import anylog_node.generic.utils_print as utils_print
import anylog_node.generic.interpreter as interpreter

file_password_ = None       # A password to protect local info on this node. i.e. list of users
global_salt_ = None

node_signatory_ = ["", "", "Node", "", ""] # Private Key, Password, Name, public key, public_key format 2 - if available signing with these keys (replacing the keys assigned to a node)
user_signatory_ = ["","","", "", ""]        # Private Key, Password, Name, public key, public_key format 2 - if available signing with these keys (replacing the keys assigned to a node)

PRIVATE_KEY_LENGTH_ = 1024

PUBLIC_KEY_LENGTH_ = 272        # The length without the header and footer and '\n' char

PUBLIC_KEY_SEGMENTS_ =[          # The segments without the header and footer and '\n' char
    #start      end     lwngth
    (27,        91,     91-27),
    (92,        156,    156-92),
    (157,       221,    221-157),
    (222,       246,    246-222)
]

PUBLIC_KEY_CHARS_ =  sum  (i[2] for i in PUBLIC_KEY_SEGMENTS_ )     # The number of chars in the public key

# ----------------------------------------------------------
# Set encryption mode to True/False
# ----------------------------------------------------------
def set_encryption(encryption):
    global use_encryption_
    use_encryption_ = encryption
# ----------------------------------------------------------
# Test encryption enabled
# ----------------------------------------------------------
def is_node_encryption():
    global use_encryption_
    return use_encryption_

# ----------------------------------------------------------
# Test if module was installed
# ----------------------------------------------------------
def is_installed():
    return  crypto_installed_
# ----------------------------------------------------------
# set authentication on/off
# If modules nolt imported - import module
# ----------------------------------------------------------
def set_node_authentication(status):
    global use_node_authentication_
    global crypto_installed_

    if status == False:
        use_node_authentication_ = False
        ret_val = process_status.SUCCESS
    else:
        # Test if the moudles were imported
        if crypto_installed_:
            use_node_authentication_ = True
            ret_val = process_status.SUCCESS
        else:
            ret_val = process_status.Failed_to_import_lib
    return ret_val
# ----------------------------------------------------------
# set authentication on/off for a user using a rest call
# Storing passwords using keyring - https://pypi.org/project/keyring/#description
# ----------------------------------------------------------
def set_user_authentication(status:process_status, user_auth_status:bool):
    global use_user_authentication_
    global file_password_
    global global_salt_

    if user_auth_status:
        # need to have a password
        if not file_password_ or not global_salt_:
            status.add_error("Missing password. Use the command 'set local password' to provide a password")
            ret_val = process_status.Missing_password
        else:
            use_user_authentication_ = True
            ret_val = process_status.SUCCESS
    else:
        use_user_authentication_ = False
        global_salt_ = None
        file_password_ = None
        ret_val = process_status.SUCCESS

    return ret_val

# ----------------------------------------------------------
# set the password of the private key.
# If in_file is true, write the password on disk encrypted by the global file_password_
# ----------------------------------------------------------
def set_prk_passwrd(status, password, in_file):
    global node_signatory_

    ret_val = process_status.SUCCESS

    if in_file:
        if not file_password_:
            status.add_error("Private key paswword can't be saved locally without local password. Use the command 'set local password' to declare local password")
            ret_val = process_status.Missing_password
        else:
            # Encrypt password using the file_password_ and write password to file
            f_object = generate_fernet(status, file_password_, global_salt_)
            ret_val, saved_password = protected_file_read(status, "!id_dir/auth.id", f_object)
            if not ret_val and not len(saved_password):
                # New file
                saved_password.append(password)
                ret_val = protected_file_write(status, "!id_dir/auth.id", saved_password, f_object)

    if not ret_val:
        node_signatory_[1] = password

    return ret_val

# ----------------------------------------------------------
# Load private key and public key from the pem file
# ----------------------------------------------------------
def load_node_keys(status):
    global node_signatory_

    node_signatory_[0] = get_node_private_key(status)   # Node_signatory is set with: Private Key, Password, Name
    if not node_signatory_[0]:
        ret_val = process_status.Private_key_not_available
    else:
        node_signatory_[3] = get_node_public_key(status)
        if not node_signatory_[3]:
            ret_val = process_status.Missing_public_key
        else:
            ret_val = process_status.SUCCESS

    return ret_val
# ----------------------------------------------------------
# Load the password of the private key
# ----------------------------------------------------------
def load_private_key_password(status):
    global node_signatory_

    if not file_password_:
        # The private key of the node is encrypted by the local password. User need to provide local password to retrieve the provate key password
        status.add_error("Node Authentication Error: Private key can't be loaded without local password. Use the command 'set local password' to declare local password")
        ret_val = process_status.Missing_password
    else:
        # Encrypt password using the file_password_ and write password to file
        f_object = generate_fernet(status, file_password_, global_salt_)
        ret_val, saved_password = protected_file_read(status, "!id_dir/auth.id", f_object)
        if not ret_val:
            if not isinstance(saved_password, list) or len(saved_password) != 1:
                ret_val = process_status.Private_key_not_available
            else:
                node_signatory_[1] = saved_password[0]
                ret_val = process_status.SUCCESS        # private key was read
    return ret_val
# ----------------------------------------------------------
# set password to encrypted data. Example of call: set local password = 123456
# Encrypts data saved in files on the node. The encryption is using a password and a random Salt.
# First call to set_aut_password generates salt and an encrypted massage.
# The encrypted massage can validate the password such that:
# If a user provides a password, and the Salt ket exists, the process can validate the password
# ----------------------------------------------------------
def set_aut_passwrd(status:process_status, password:str):
    '''
    Set password to encrypted data
    1. Save the file password provided by the user as a global variable.
    2. If there is no Salt key - generate Salt, write Salt in file and place Salt as a global variable.
    3. If Salt key exists and read from file, test that the password provided is correct
    '''

    global file_password_
    global global_salt_

    test_string = b"1234567890AnyLog1234567890"

    # Read the salt file and if missing - make a salt
    file_name = params.get_value_if_available("!id_dir/frame.id")
    ret_val, salt_test = utils_io.read_protected_file(status, file_name)    # salt_test: 16 bytes of salt + 26 bytes of test_stryng encrypted
    if ret_val == process_status.File_read_failed:
        # No such file, otherwise Salt exists
        # Create and write the salt
        file_password_ = password
        global_salt_ = os.urandom(16)
        fernet_object = generate_fernet(status, file_password_, global_salt_)
        symetric = fernet_object.encrypt(test_string)
        ret_val = utils_io.write_protected_file(status, file_name, global_salt_ + symetric)
    else:
        # Test the password by decrypting the encrypted test_string
        salt = salt_test[:16]
        encrypted_str = salt_test[16:]
        fernet_object = generate_fernet(status, password, salt)
        try:
            decrypt_data = fernet_object.decrypt(encrypted_str)
        except:
            ret_val = process_status.Wrong_password
        else:
            if decrypt_data == test_string:
                global_salt_ = salt
                file_password_ = password
                ret_val = process_status.SUCCESS
            else:
                ret_val = process_status.Wrong_password

    return ret_val
# ----------------------------------------------------------
# Test for user authentication flag
# ----------------------------------------------------------
def is_user_authentication():
    global use_user_authentication_
    return use_user_authentication_
# ----------------------------------------------------------
# Test for node authentication flag
# ----------------------------------------------------------
def is_node_authentication():
    global use_node_authentication_
    return use_node_authentication_

# ----------------------------------------------------------
# Return the signatory name
# ----------------------------------------------------------
def get_signatory_name():
    global user_signatory_
    return user_signatory_[2]

# ----------------------------------------------------------
# Replace the nodes key to sign messages.
# Use a different private key to sign messages and policies
# ----------------------------------------------------------
def set_signatory(private_key, password, name):
    global user_signatory_
    public_key = public_from_private(private_key, password)
    if public_key:
        # Key and password match
        user_signatory_[0] = private_key
        user_signatory_[1] = password
        user_signatory_[2] = name
        user_signatory_[3] = public_key     # Public key with headers
        user_signatory_[4] = get_public_key_chars(public_key) # Public key format 2 - without headers
        ret_val = process_status.SUCCESS
    else:
        ret_val = process_status.Wrong_password
    return ret_val
# ----------------------------------------------------------
# Revert to set the node as the signatory.
# If the values not available, the node will sign the messages and policies
# ----------------------------------------------------------
def reset_signatory(status, io_buff_in, cmd_words, trace):
    global user_signatory_
    user_signatory_[0] = ""
    user_signatory_[1] = ""
    user_signatory_[2] = ""
    user_signatory_[3] = ""
    user_signatory_[4] = ""
    return process_status.SUCCESS
# ----------------------------------------------------------
# Return the signatory name (or the node as a signatory)
# ----------------------------------------------------------
def get_signatory(status, io_buff_in, cmd_words, trace):
    global user_signatory_
    signatory_name = user_signatory_[2]
    if not signatory_name:
        if node_signatory_[0]:
            signatory_name = "Current Node (%s)" % params.get_node_name()
        else:
            signatory_name = "No signatory assigned"
    return [process_status.SUCCESS, signatory_name]
# ----------------------------------------------------------
# Is message encryption
# ----------------------------------------------------------
def get_encryption():
    global use_encryption_

    if use_encryption_:
        reply = "Node Encryption: On"
    else:
        reply = "Node Encryption: Off"
    return reply
# ----------------------------------------------------------
# Get the status of the authentication
# ----------------------------------------------------------
def get_authentication():
    global use_node_authentication_
    global use_user_authentication_
    global crypto_installed_

    if crypto_installed_:
        if use_node_authentication_:
            signatory_name = user_signatory_[2] if user_signatory_[2] else "Node"
            reply = f"Node Authentication: On (Signatory: {signatory_name})"
        else:
            reply = "Node Authentication: Off"
    else:
        reply = "Node Authentication is off - Failed to import 'cryptography'"

    basic_auth = "On" if  use_user_authentication_ else "Off"
    reply += f"\r\nUser Basic Authentication: {basic_auth}"

    return reply
# ----------------------------------------------------------
# Create a public and private keys
# ----------------------------------------------------------
def create_keys(password):

    try:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=PRIVATE_KEY_LENGTH_, backend=default_backend())
        public_key = private_key.public_key()

        if password:
            passwd = password.encode('ascii')
            private_bytes = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                      format=serialization.PrivateFormat.PKCS8,
                                                      encryption_algorithm=serialization.BestAvailableEncryption(passwd))
        else:
            private_bytes = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                      format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                      encryption_algorithm=serialization.NoEncryption())

        public_bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                               format=serialization.PublicFormat.SubjectPublicKeyInfo)


        private_str = private_bytes.decode("utf-8")
        public_str = public_bytes.decode("utf-8")

    except:
        private_str = ""
        public_str = ""


    return [private_str, public_str]

# ----------------------------------------------------------
# Get the public key from the private key
# ----------------------------------------------------------
def public_from_private(private_str, password):
    private_key = priv_str_to_key(private_str, password)

    try:
        public_key = private_key.public_key()
        public_bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                               format=serialization.PublicFormat.SubjectPublicKeyInfo)
        public_str = public_bytes.decode("utf-8")
    except:
        public_str = ""

    return public_str


# ----------------------------------------------------------
# Reverse private key string structure to a private key object
# ----------------------------------------------------------
def priv_str_to_key(private_str, password):
    '''
     Return object type RSAPrivateKey
     '''

    if not password:
        passwd_in = None
    else:
        passwd_in = password.encode('ascii')

    if private_str:
        pvt_key_in = private_str.encode('ascii')

        try:
            private_key = serialization.load_pem_private_key(pvt_key_in, password=passwd_in, backend=default_backend())
        except:
            private_key = None
    else:
        private_key = None

    return private_key


# ----------------------------------------------------------
# Reverse public key string structure to a public key object
# ----------------------------------------------------------
def public_str_to_key(public_str):
    '''
    Return object type RSAPublicKey
    '''

    plc_key = public_str.encode('ascii')
    try:
        public_key = load_pem_public_key(plc_key, backend=default_backend())
    except:
        errno, value = sys.exc_info()[:2]
        public_key = None

    return public_key


# ----------------------------------------------------------
# Sign a message
# ----------------------------------------------------------
def sign(status:process_status, private_str: str, password: str, msg: str):
    try:
        private_key = priv_str_to_key(private_str, password)
        message = msg.encode('ascii')

        signature_bytes = private_key.sign(message, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                                salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

        signature_hex = binascii.b2a_hex(signature_bytes)
        signature = str(signature_hex, "utf-8")
    except:
        errno, value = sys.exc_info()[:2]
        status.add_error("Signature error: %s" % str(value))
        signature = ""

    return signature

# ----------------------------------------------------------
# Verify a message
# - Using the public key, verify that the owner of the private key signed the message
# ----------------------------------------------------------
def verify(public_str: str, sig: str, msg: str):
    public_key = public_str_to_key(public_str)
    if not public_key:
        ret_val = False
    else:
        try:
            message = msg.encode('ascii')
            signature_hex = sig.encode('ascii')
            signature = binascii.a2b_hex(signature_hex)

            public_key.verify(signature, message,
                              padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                              hashes.SHA256())
        except:
            errno, value = sys.exc_info()[:2]
            ret_val = False
        else:
            ret_val = True

    return ret_val

# ----------------------------------------------------------
# Given a node message -
# a) Create a password and a salt (16 bytes + 16 bytes)
# b) Encrypt the password and the seed using a public key of the receiver
# c) Encrypt the message using symetric encryption
# d) Return encrypted passwords + encrypted message
# ----------------------------------------------------------
def encrypt_node_message(status: process_status, public_str: str, data: str):

    public_key = str_values_to_public_str(public_str)

    key = secrets.token_urlsafe(32)     # 16 first bytes are the key and the second 16 bytes are the salt

    asymetric = encrypt(status, public_key, key)

    # encrypt the data using the self generated password and salt
    f_object = generate_fernet(status, key[:16], key[16:].encode())

    b_data = data.encode()
    try:
        symetric = f_object.encrypt(b_data)
    except:
        status.add_error("Encryption of message failed")
        symetric = None

    return [asymetric, symetric]

# ----------------------------------------------------------
# Symetric encryption of data
# ----------------------------------------------------------
def symetric_encryption(status, f_object, data):

    b_data = data.encode()
    try:
        encrypted = f_object.encrypt(b_data)
    except:
        status.add_error("Encryption of message failed")
        encrypted = None

    return encrypted

# ----------------------------------------------------------
# Symetric encryption of data
# ----------------------------------------------------------
def symetric_decryption(status, f_object, data):

    b_data = data.encode()
    try:
        decrypt_data = f_object.decrypt(b_data)
    except:
        status.add_error("Failed to decrypt message data")
        data_str = None
    else:
        data_str = decrypt_data.decode()


    return data_str
# ----------------------------------------------------------
# Make a Password (16 bytes) + salt (16 bytes)
# Make an encrypted key (16 bytes password and 15 bytes salt) (asymmetric encryption))
# Use the Password and Salt to generate an encryption object
# Return encrypted key and the Fernet object
# The encrypted key is send to the receiver to decrypt the password (and salt) using the private key.
# ----------------------------------------------------------
def setup_encryption(status: process_status, public_str: str):

    public_key = str_values_to_public_str(public_str)

    key = secrets.token_urlsafe(32)     # 16 first bytes are the key and the second 16 bytes are the salt

    encrypted_key = encrypt(status, public_key, key)    # Encrypt using the public key of the receiver of the message

    # encrypt the data using the self generated password and salt
    f_object = generate_fernet(status, key[:16], key[16:].encode())

    return [encrypted_key, f_object]

# ----------------------------------------------------------
# Given an encrypted node message
# a) Using the node private key decrypt the password and a salt (16 bytes + 16 bytes)
# b) Using the password and salt decrypt the data
# ----------------------------------------------------------
def decrypt_node_message(status: process_status, ciphertext: str):

    global node_signatory_

    if not node_signatory_[1]:
        # try to load the password from file
        ret_val = load_private_key_password(status)
    else:
        ret_val = process_status.SUCCESS

    if not ret_val:

        if not node_signatory_[0]:
            ret_val = load_node_keys(status)
        else:
            ret_val = process_status.SUCCESS

        if not ret_val:
            plaintext = decrypt(status, node_signatory_[0], node_signatory_[1], ciphertext)
        else:
            plaintext = ""
    else:
        plaintext = ""

    return plaintext
# ----------------------------------------------------------
# Encryption - Asymetric Encryption
# ----------------------------------------------------------
def encrypt(status: process_status, public_str: str, msg: str):

    public_key = public_str_to_key(public_str)
    if not public_key:
        ciphertext = ""
    else:
        try:
            message = msg.encode('ascii')
            cipher_bytes = public_key.encrypt(message,
                                              padding.OAEP(
                                                  mgf=padding.MGF1(algorithm=hashes.SHA256()),  # SHA1
                                                    algorithm=hashes.SHA256(),                  # SHA1
                                                  label=None))

            cipher_hex = binascii.b2a_hex(cipher_bytes)
            ciphertext = str(cipher_hex, "utf-8")

        except:
            errno, value = sys.exc_info()[:2]
            status.add_error("Encryption error: %s" % str(value))
            ciphertext = ""

    return ciphertext
# ----------------------------------------------------------
# Decryption - Asymetric Decryption
# ----------------------------------------------------------
def decrypt(status: process_status, private_str: str, password: str, ciphertext: str):

    private_key = priv_str_to_key(private_str, password)

    if private_key and ciphertext:
        # ciphertext_bytes = ciphertext.encode('ascii')
        ciphertext_bytes = ciphertext.encode('utf-8')
        cipher_hex_bytes = binascii.unhexlify(ciphertext_bytes)

        try:
            text_bytes = private_key.decrypt(cipher_hex_bytes, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),   # SHA1
                                                                            algorithm=hashes.SHA256(), label=None))     # SHA1
        except:
            errno, value = sys.exc_info()[:2]
            status.add_error("Decryption error: %s" % str(value))
            plaintext = ""
        else:
            plaintext = text_bytes.decode("utf-8")
    else:
        plaintext = ""

    return plaintext


# =======================================================================================================================
# Craete a private and public key and store in a file
# =======================================================================================================================
def create_keys_to_file(status, password, keys_file):
    dir_name, file_name, file_type = utils_io.extract_path_name_type(keys_file)
    if not dir_name:
        # use default dir
        dir_name = params.get_value_if_available("!id_dir")
    if not file_name:
        file_name = "keys_file"
    if not file_type:
        file_name += ".pem"

    private_str, public_str = create_keys(password)

    if not private_str or not public_str:
        ret_val = process_status.Failed_to_generate_keys
    else:
        ret_val = keys_to_file(status, public_str, private_str, dir_name, file_name, True)

    return ret_val


# =======================================================================================================================
# Craete a node ID - create new set of Private and Public Keys and maintain keys on disk
# Private key is encrypted
# =======================================================================================================================
def create_node_id(status, password, ignore_error):

    global node_signatory_

    if get_node_public_key(status):
        # Node ID exists
        if ignore_error:
            ret_val = process_status.SUCCESS  # Return success as a script may start with create key - the call is being ignored as the node has keys.
        else:
            status.add_error("Keys for this node already created")
            ret_val = process_status.ERR_process_failure
    else:
        if not password:
            # Must have password
            ret_val = process_status.Missing_password
        else:
            private_str, public_str = create_keys(password)
            if not private_str or not public_str:
                ret_val = process_status.Failed_to_generate_keys
            else:
                dir_name = params.get_value_if_available("!id_dir")
                # Save Public key + Private Key in a file
                ret_val = keys_to_file(status, public_str, private_str, dir_name, "node_id.pem", True)
                if not ret_val:
                    node_signatory_[0] = private_str
                    node_signatory_[3] = public_str

    return ret_val

# =======================================================================================================================
# Write the encrypted private key and the public key to file
# =======================================================================================================================
def keys_to_file(status, public_str, private_str, d_name, f_name, create_dir):

    info = public_str + private_str
    if d_name[-1] != "/" and d_name[-1] != '\\':
        dir_name = d_name + params.get_path_separator()
    else:
        dir_name = d_name
    file_name = dir_name + f_name

    ret_val = utils_io.test_dir_exists(status, dir_name, False)
    if ret_val == process_status.ERR_dir_does_not_exists:
        # directory does not exists - test flag to determine if to create the needed directory
        if create_dir:
            ret_val = process_status.SUCCESS
            if not utils_io.create_dir(status, dir_name):
                status.add_error("Failed to create a directory: %s" % dir_name)
                ret_val = process_status.Failed_to_create_dir

    if not ret_val:
        # dir exists or created
        if not utils_io.write_str_to_file(status, info, file_name):
            status.add_error("Failed to write keys or file already exists: %s" % file_name)
            ret_val = process_status.File_write_failed
        else:
            utils_io.change_mode(file_name, 0o444)  # make the file read only

    return ret_val


# =======================================================================================================================
# Return the public key
# =======================================================================================================================
def get_node_public_key(status):
    dir_name = params.get_value_if_available("!id_dir")
    file_name = dir_name + params.get_path_separator() + "node_id.pem"
    public_key = read_pem_file(status, file_name, False)

    return public_key
# =======================================================================================================================
# Return Unique Node ID - (formatted PK)
# The node ID is the Public Key assigned to the node
# =======================================================================================================================
def get_node_id(status):

    global node_signatory_

    if node_signatory_[4]:
        node_id = node_signatory_[4]
    else:
        if not node_signatory_[3]:
            # read from file
            node_signatory_[3] = get_node_public_key(status)

        if not node_signatory_[4]:
            # get without the "PUBLIC KEY" header
            node_id = get_public_key_chars(node_signatory_[3])
            node_signatory_[4] = node_id
        else:
            node_id = node_signatory_[4]

    return node_id

# =======================================================================================================================
# Remove Header, footer and '\n' chars from the bublic key
# =======================================================================================================================
def get_public_key_chars(public_key):

    if len(public_key) == PUBLIC_KEY_LENGTH_:
        # without header and footer and '\n
        # For performance - assume standard size first
        public_string = ""
        for entry in PUBLIC_KEY_SEGMENTS_:
            start_offset = entry[0]
            end_offset = entry[1]
            public_string += public_key[start_offset:end_offset]
    else:
        # Remove the "-----BEGIN ..." and "-----END ...." headers
        offset_start = public_key.find("KEY-----")  # Find -----BEGIN ENCRYPTED PRIVATE KEY----- or "-----BEGIN PUBLIC KEY-----"
        if offset_start > 0:
            offset_end = public_key.rfind("-----END ")  # Find ----------END ENCRYPTED PRIVATE KEY---------- or "-----END PUBLIC KEY-----"
            if offset_end > 0:
                public_string = public_key[offset_start + 8:offset_end].replace("\n", "")
            else:
                public_string = ""
        else:
            public_string = public_key      # Keep as is

    return public_string
# =======================================================================================================================
# Read from a .pem file
# Lines 0-5 are the public key and lines 6-24 are the private key
# =======================================================================================================================
def read_pem_file(status, file_name, is_private_key):

    if is_private_key:
        start_line = 6
        end_line = 24
        key_name = "private"
        key_length = 1074
    else:
        start_line = 0
        key_name = "public"


    data_read = utils_io.read_all_lines_in_file(status, file_name)
    if data_read:
        if key_name == "public":
            if len(data_read) > 9 and data_read[8] == "-----END PUBLIC KEY-----":
                end_line = 10       # This is the public key generated for the certificate in a command: id generate certificate request
                key_length = 452
            else:
                end_line = 6        # A public key generated from a command:  id create keys
                key_length = PUBLIC_KEY_LENGTH_

        if not data_read or len(data_read) < end_line:
            pem_key = ""
            status.add_error("File '%s' does not contain a %s key" % (file_name, key_name))
        else:
            pem_key = '\n'.join(data_read[start_line:end_line])
            pem_key += '\n'

            if len(pem_key) != key_length:
                pem_key = ""
                status.add_error("Wrong %s key structure in file '%s'" % (key_name, file_name))
    else:
        status.add_error("Failed to read key from file '%s'" % (file_name))
        pem_key = ""

    return pem_key

# =======================================================================================================================
# Return Unique Node ID
# The node ID is the Public Key assigned to the node
# =======================================================================================================================
def get_node_private_key(status):

    dir_name = params.get_value_if_available("!id_dir")
    file_name = dir_name + params.get_path_separator() + "node_id.pem"

    private_key = read_pem_file(status, file_name, True)

    return private_key

# =======================================================================================================================
# Return hardware ID
# =======================================================================================================================
def get_hardware_id():
    try:
        if sys.platform.startswith('win'):
            reply = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
        else:
            # reply = subprocess.Popen('hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid'.split())
            reply = get_platform()
    except OSError as e:
        reply = "Failed to retrieve unique id: %s" % str(e)
    except:
        reply = "Failed to retrieve unique id"

    return reply


# =======================================================================================================================
# Return Unique Node ID
# =======================================================================================================================
def get_platform():
    try:
        process = subprocess.Popen("cat /var/lib/dbus/machine-id", shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    except:
        node_info = uuid.getnode()  # use another method
    else:
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        except:
            node_info = uuid.getnode()  # use another method
        else:
            if len(stderr):
                node_info = uuid.getnode()
            else:
                node_info = stdout.decode("utf-8")
                if node_info and node_info[-1] == '\n':
                    node_info = node_info[:-1]

    return node_info
# =======================================================================================================================
# If a user is the signatory, take the public key from the user.
# Otherwise, use the public key of the node
# =======================================================================================================================
def get_signatory_public_key(status):

    global node_signatory_
    global user_signatory_

    ret_val = process_status.SUCCESS
    if user_signatory_[4]:
        public_key = user_signatory_[4]
    else:
        if not node_signatory_[4]:
            public_key = get_node_id(status)
            if not public_key:
                ret_val = process_status.Missing_public_key
        else:
            public_key = node_signatory_[4]
    return [ret_val, public_key]

# =======================================================================================================================
# Get authentication string - sign a string and provide the following:
# Public key, signature, string signed.
# in the case of a message: [Public Key] [Signature] [ip + port + time]
# =======================================================================================================================
def make_auth_str(status, info_string):

    global node_signatory_
    global user_signatory_

    signed_str = None
    if user_signatory_[0]:
        # Use the user signatory (a user was assigned using the command: set signatory ...)
        signatory = user_signatory_
        ret_val = process_status.SUCCESS
    else:
        # Use the node as signatory
        signatory = node_signatory_
        if not node_signatory_[1]:
            # try to load the password from file
            ret_val = load_private_key_password(status)
        else:
            ret_val = process_status.SUCCESS

        if not ret_val:
            if not node_signatory_[0]:
                # Load the private and public keys from the file
                ret_val = load_node_keys(status)

    if not ret_val:
        signature = sign(status, signatory[0], signatory[1], info_string)
        if not signature:
            ret_val = process_status.Failed_message_sign
        else:
            signed_str = signature + info_string

    return [ret_val, signed_str]


# =======================================================================================================================
# Get the transfer string - the string that is passed to the peer node for authentication
# =======================================================================================================================
def get_transfer_str(status, source_data):
    '''
    status - user status object
    source_data - the data which is signed together with the date and time. i.e. ip:port
    '''
    # Node authentication - sign a message such that the receiver node can authenticate the sender and the authorization
    auth_str = ""
    ret_val = process_status.SUCCESS
    if is_node_authentication():
        # public_str = al_auth.get_node_id(status)
        ret_val, public_str = get_signatory_public_key(status)  # Get the active public key (of the user or the node)
        if not ret_val:
            if public_str:
                # get  a string that includes the signature + the message signed
                ret_val, signed_str = make_auth_str(status, source_data + "-" + str(get_current_time_in_sec()))  # get authentication string based on the IP and port
                if not ret_val:
                    auth_str = public_str + signed_str  # add the public key
            else:
                ret_val = process_status.Missing_public_key
    elif is_node_encryption():
        # The returned data needs to be encrypted - push the public key to the authentication string (the receiver will use the public key for encryption)
        auth_str = get_node_id(status)  # only send the public key
        if not auth_str:
            ret_val = process_status.Missing_public_key

    return [ret_val, auth_str]

# =======================================================================================================================
# Unpack authentication string to return:
# Public key
# Signature,
# Signed mesage
# =======================================================================================================================
def unpack_auth_str(auth_string):

    public_str = str_values_to_public_str(auth_string)

    signature = auth_string[PUBLIC_KEY_CHARS_:PUBLIC_KEY_CHARS_ + 256]

    signed_message = auth_string[PUBLIC_KEY_CHARS_ + 256 :]

    return [public_str, signature, signed_message]

# =======================================================================================================================
# Add suffix and prefix to public key string values
# The input string may be longer than the bytes needed - only consider the first bytes
# =======================================================================================================================
def str_values_to_public_str(str_values):

    public_str = '-----BEGIN PUBLIC KEY-----\n'
    index = 0
    for entry in PUBLIC_KEY_SEGMENTS_:
        segment_length = entry[2]
        public_str += (str_values[index:index + segment_length] + '\n')
        index += segment_length

    public_str += '-----END PUBLIC KEY-----\n'

    return public_str

# =======================================================================================================================
# Return the list of users
# =======================================================================================================================
def get_users_list(status):

    reply = ""
    if not use_user_authentication_:
        ret_val = process_status.user_auth_disabled
    elif not file_password_:
        ret_val = process_status.Missing_password
    else:
        f_object = generate_fernet(status, file_password_, global_salt_)
        ret_val, all_users = protected_file_read(status, "!id_dir/users.id", f_object)
        if not ret_val:
            reply_info = []
            for entry in all_users:
                expiration = entry["expiration"]
                if not expiration:
                    time_limit = "Unlimited"
                else:
                    current_utc = get_current_time_in_sec()
                    if expiration <= current_utc:
                        time_limit = "Expired"
                    else:
                        time_limit = get_date_time_from_utc_sec(expiration, "%Y-%m-%d %H:%M:%S")
                reply_info.append((entry["name"], entry["type"], time_limit))
            reply = utils_print.output_nested_lists(reply_info, "", ["User Name", "User Type", "Time Limit"], True)

    return [ret_val, reply]
# =======================================================================================================================
# Update local users with the following:
# user name, password, seconds to termination
# =======================================================================================================================
def remove_local_user(status, user_name):

    if not use_user_authentication_:
        ret_val = process_status.user_auth_disabled
    elif not file_password_:
        ret_val = process_status.Missing_password
    else:
        f_object = generate_fernet(status, file_password_, global_salt_)
        ret_val, all_users = protected_file_read(status, "!id_dir/users.id", f_object)
        if not ret_val:
            if get_user_info(status, all_users, user_name, None, False):
                # test that the user name does not exists:
                for index, json_obj in enumerate(all_users):
                    if test_key_value(json_obj, "name", user_name):
                        del all_users[index]
                        ret_val = protected_file_write(status, "!id_dir/users.id", all_users, f_object)
                        break
            else:
                ret_val = process_status.Wrong_username_passwd

    return ret_val

# =======================================================================================================================
# Update password
# =======================================================================================================================
def update_local_user_password(status, user_name, old_password, new_password):

    global use_user_authentication_
    global file_password_
    global global_salt_

    if not use_user_authentication_:
        ret_val = process_status.user_auth_disabled
    elif not file_password_:
        ret_val = process_status.Missing_password
    else:
        f_object = generate_fernet(status, file_password_, global_salt_)
        ret_val, list_data = protected_file_read(status, "!id_dir/users.id", f_object)
        if not ret_val:
            # test that the user name does not exists:
            user_info = get_user_info(status, list_data, user_name, old_password, True)
            if user_info:
                user_info["password"] = new_password
                ret_val = protected_file_write(status, "!id_dir/users.id", list_data, f_object)
            else:
                ret_val = process_status.Wrong_username_passwd

    return ret_val
# =======================================================================================================================
# Update local users with the following:
# user name, password, seconds to termination
# Call usage: id add user where name = ori and password = 123 and expiration = 2 minutes
# =======================================================================================================================
def add_local_user(status, user_name, user_type, password, expiration):

    global use_user_authentication_
    global file_password_
    global global_salt_

    if not use_user_authentication_:
        ret_val = process_status.user_auth_disabled
    elif not file_password_:
        ret_val = process_status.Missing_password
    else:
        f_object = generate_fernet(status, file_password_, global_salt_)
        ret_val, list_data = protected_file_read(status, "!id_dir/users.id", f_object)

        if not ret_val:
            # test that the user name does not exists:
            if get_user_info(status, list_data, user_name, None, False):
                ret_val = process_status.User_name_exists
            else:

                if expiration:
                    expiration_time =  get_current_time_in_sec() + expiration
                else:
                    expiration_time = 0

                user_info = {
                    "service" : "users",        # Indication of user name and password
                    "name" : user_name,
                    "password" : password,
                    "expiration" : expiration_time,
                    "type" : user_type,
                }

                list_data.append(user_info)

                ret_val = protected_file_write(status, "!id_dir/users.id", list_data , f_object)

                if ret_val:
                    ret_val = process_status.Failed_to_add_new_user

    return ret_val
# =======================================================================================================================
# Get user info from the users file
# =======================================================================================================================
def get_user_info(status, all_users, user_name, user_password, consider_time):

    user_obj = None
    if all_users:
        # search is the user exists
        for json_obj in all_users:
            if test_key_value(json_obj, "name", user_name):
                if not user_password or test_key_value(json_obj, "password", user_password):
                    if consider_time:
                        expiration = json_obj["expiration"]
                        if not expiration or expiration > get_current_time_in_sec():
                            # Test expiration
                            user_obj = json_obj  # returned user info
                    else:
                        user_obj = json_obj  # returned user info
                    break
    return user_obj

# =======================================================================================================================
# Test if the key maps to a user and password in the file
# Called from the REST API
# =======================================================================================================================
def validate_basic_auth(status, user_name, password):

    if is_user_authentication():
        if user_name and password:
            ret_val = test_user_password(status, user_name, password)
        else:
            ret_val = False
    else:
        ret_val = True
    return ret_val

# =======================================================================================================================
# Test if the key maps to a user and password in the file
# Called from the REST API
# =======================================================================================================================
def validate_user(status, user_key, test_expiration):

    if user_key and isinstance(user_key, str):
        if user_key.startswith("Basic "):
            key = user_key[6:]
        else:
            key = user_key
        encoded_bytes = key.encode('ascii')
        decoded_bytes = base64.b64decode(encoded_bytes)
        user_password = decoded_bytes.decode("utf-8")

        ret_val = False
        index = user_password.find(':')
        if index > 0 and index < (len(user_password) - 1):
            user_name = user_password[:index]
            password = user_password[index + 1:]

            ret_val = test_user_password(status, user_name, password)

    else:
        ret_val = False

    return ret_val

# =======================================================================================================================
# Test the user  name and password against the encrypted data
# =======================================================================================================================
def test_user_password(status, user_name, password):
    f_object = generate_fernet(status, file_password_, global_salt_)
    ret_val, list_data = protected_file_read(status, "!id_dir/users.id", f_object)
    if not ret_val:
        # test that the user name does not exists:
        if get_user_info(status, list_data, user_name, password, True):
            ret_val = True
        else:
            ret_val = False
    else:
        ret_val = False
    return ret_val

# =======================================================================================================================
# =======================================================================================================================
# Generate a certificate
# https://www.jython.org/jython-old-sites/docs/library/ssl.html#ssl-certificates
# =======================================================================================================================
# =======================================================================================================================

# =======================================================================================================================
# Generate the private key and the public key for the certificate authority
# =======================================================================================================================
def generate_certificate_authority(status, conditions):

    ret_val = process_status.SUCCESS
    directory_name = params.get_value_if_available("!pem_dir") + params.get_path_separator()

    passphrase = interpreter.get_one_value_or_default(conditions, "password", None)
    org = interpreter.get_one_value_or_default(conditions, "org", "anylog")

    file_key = org.strip().lower().replace(" ", "-")  # replace spaces with '-' sign

    ca_public_key = directory_name + "ca-%s-public-key.crt" % file_key
    ca_private_key = directory_name + "ca-%s-private-key.key" % file_key

    country = interpreter.get_one_value_or_default(conditions, "country", "US")
    state = interpreter.get_one_value_or_default(conditions, "state", "CA")
    locality = interpreter.get_one_value_or_default(conditions, "locality", "Redwood City")

    hostname = interpreter.get_one_value_or_default(conditions, "hostname", "anylog.co")

    private_key = _generate_private_key(status, ca_private_key, passphrase)
    if not private_key:
        status.add_error("Failed to generate private key")
        ret_val = process_status.ERR_process_failure
    else:
        public_key = _generate_public_key(status, private_key,
                            filename = ca_public_key,
                             country = country,
                             state = state,
                             locality = locality,
                             org = org,
                             hostname = hostname )
        if not public_key:
            status.add_error("Failed to generate public key")
            ret_val = process_status.ERR_process_failure

    return ret_val

# =======================================================================================================================
# Generate a certificate request
# =======================================================================================================================
def generate_certificate_request(status, conditions):

    ret_val = process_status.SUCCESS

    passphrase = interpreter.get_one_value_or_default(conditions, "password", None)
    org = interpreter.get_one_value_or_default(conditions, "org", "anylog")

    file_key = org.strip().lower().replace(" ", "-")  # replace spaces with '-' sign

    directory_name = params.get_value_if_available("!pem_dir") + params.get_path_separator()

    server_csr = directory_name + "server-%s-csr.csr" % file_key
    server_private_key_file = directory_name + "server-%s-private-key.key" % file_key
    server_public_key_file = directory_name + "server-%s-public-key.pem" % file_key     # The public key that determines the permissions on the blockchain

    country = interpreter.get_one_value_or_default(conditions, "country", "US")
    state = interpreter.get_one_value_or_default(conditions, "state", "CA")
    locality = interpreter.get_one_value_or_default(conditions, "locality", "RWC")

    alt_names = interpreter.get_one_value_or_default(conditions, "alt_names", "localhost")
    hostname = interpreter.get_one_value_or_default(conditions, "hostname", "my-site.com")
    ip = interpreter.get_one_value_or_default(conditions, "ip", "192.56.76.4")

    # Generate a key used by the server to sign the certificate request when it is send to a peer node
    server_private_key = _generate_private_key(status, server_private_key_file, passphrase)

    if not server_private_key:
        status.add_error("Failed to generate private key")
        ret_val = process_status.ERR_process_failure
    else:

        try:
            server_public_key = server_private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
        except:
            errno, value = sys.exc_info()[:2]
            status.add_error("Failed to generate public key from the private key of the external server with error: '%s' - '%s'" % (errno, value))
            ret_val = process_status.ERR_process_failure
        else:
                # Write the server public key
                # This is the public key that determines the permissions for the application (on the blockchain)
                try:
                    with open(server_public_key_file, "wb") as keyfile:
                        keyfile.write(server_public_key)
                except:
                    errno, value = sys.exc_info()[:2]
                    message = "Failed to write the spublic key of the external server to file: '%s' with error %s: %s" % (
                    server_public_key_file, str(errno), str(value))
                    status.add_error(message)
                    ret_val = process_status.ERR_process_failure
                else:

                    # generate the certificate request
                    csr = _generate_csr(status, server_private_key,
                                  filename = server_csr,
                                  country = country,
                                  state = state,
                                  locality = locality,
                                  org = org,
                                  alt_names = [alt_names],
                                  hostname = hostname,
                                  ip=ip)

                    if not csr:
                        status.add_error("Failed to generate public key")
                        ret_val = process_status.ERR_process_failure

    return ret_val

# =======================================================================================================================
# Sign a certificate request
# =======================================================================================================================
def sign_certificate_request(status, conditions):

    directory_name = params.get_value_if_available("!pem_dir") + params.get_path_separator()

    server_org = interpreter.get_one_value(conditions, "server_org")
    file_key = server_org.strip().lower().replace(" ", "-")  # replace spaces with '-' sign
    server_csr = directory_name + "server-%s-csr.csr" % file_key                # The file with the certificate request
    server_public_key = directory_name + "server-%s-public-key.crt"  % file_key # the file with the signed certificate

    ca_org = interpreter.get_one_value(conditions, "ca_org")
    file_key = ca_org.strip().lower().replace(" ", "-")  # replace spaces with '-' sign
    ca_public_key_file = directory_name + "ca-%s-public-key.crt" % file_key     # Public key of the CA
    ca_private_key_file = directory_name + "ca-%s-private-key.key" % file_key   # Private key of the CA
    # Load the certificate request
    try:
        with open(server_csr, "rb") as csr_file:
            csr = x509.load_pem_x509_csr(csr_file.read(), default_backend())
    except:
        errno, value = sys.exc_info()[:2]
        status.add_error("Failed to load Certificate Sign Request (CSR) with error: '%s' - '%s'" % (errno, value))
        ret_val = process_status.ERR_process_failure
    else:
        # Load the certificate authority public key
        try:
            with open(ca_public_key_file, "rb") as key_file:
                ca_public_key = x509.load_pem_x509_certificate(key_file.read(), default_backend() )
        except:
            errno, value = sys.exc_info()[:2]
            status.add_error("Failed to load the public key of the certificate authority with error: '%s' - '%s'" % (errno, value))
            status.add_error("Failed to load the public key of the certificate authority from: %s" % (directory_name + "ca-public-key.crt"))
            ret_val = process_status.ERR_process_failure
        else:
            # Load the certificate authority private key
            try:
                with open(ca_private_key_file, "rb") as key_file:

                    # ca_private_key = serialization.load_pem_private_key(ca_private_key_file.read(), getpass().encode("utf-8"), default_backend())
                    ca_private_key = serialization.load_pem_private_key(data=key_file.read(),
                                                                        # password="1".encode("utf-8"),
                                                                        password = None,
                                                                        backend=default_backend())
            except:
                errno, value = sys.exc_info()[:2]
                status.add_error("Failed to load the private key of the certificate authority with error: '%s' - '%s'" % (errno, value))
                status.add_error("Failed to load the private key of the certificate authority from: %s" % (ca_private_key_file))
                ret_val = process_status.ERR_process_failure
            else:
                ret_val = _sign_csr(status, csr, ca_public_key, ca_private_key, server_public_key)
    return ret_val

# =======================================================================================================================
# Sign a certificate signing request
# =======================================================================================================================
def _sign_csr(status, csr, ca_public_key, ca_private_key, new_filename):
    ret_val = process_status.SUCCESS
    valid_from = datetime.utcnow()
    valid_until = valid_from + timedelta(days=30)

    builder = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(ca_public_key.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(valid_from)
        .not_valid_after(valid_until)
    )
    # copy any extensions that were set on the CSR.
    for extension in csr.extensions:
        builder = builder.add_extension(extension.value, extension.critical)
    # signs the public key with the CA’s private key.
    try:
        public_key = builder.sign(
            private_key=ca_private_key,
            algorithm=hashes.SHA256(),
            backend=default_backend(),
        )
    except:
        status.add_error("Failed to sign certificate request")
        ret_val = process_status.ERR_process_failure
    else:
        try:
            with open(new_filename, "wb") as keyfile:
                keyfile.write(public_key.public_bytes(serialization.Encoding.PEM))
        except:
            errno, value = sys.exc_info()[:2]
            message = "Failed to write the signed certificate request at: '%s' with error %s: %s" % (new_filename, str(errno), str(value))
            status.add_error(message)
            ret_val = process_status.ERR_process_failure
    return ret_val



# =======================================================================================================================
# Generate a certificate signing request
# =======================================================================================================================
def _generate_csr(status, private_key, filename, **kwargs):
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, kwargs["country"]),
            x509.NameAttribute(
                NameOID.STATE_OR_PROVINCE_NAME, kwargs["state"]
            ),
            x509.NameAttribute(NameOID.LOCALITY_NAME, kwargs["locality"]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, kwargs["org"]),
            x509.NameAttribute(NameOID.COMMON_NAME, kwargs["hostname"]),
            x509.NameAttribute(NameOID.GIVEN_NAME, kwargs["ip"])
        ]
    )

    # Generate any alternative dns names
    alt_names = []
    for name in kwargs.get("alt_names", []):
        alt_names.append(x509.DNSName(name))
    san = x509.SubjectAlternativeName(alt_names)

    builder = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(subject)
        .add_extension(san, critical=False)
    )
    try:
        csr = builder.sign(private_key, hashes.SHA256(), default_backend())
    except:
        status.add_eror("Failed to sign a Certificate Signing Request")
        csr = None
    else:
        try:
            with open(filename, "wb") as csrfile:
                csrfile.write(csr.public_bytes(serialization.Encoding.PEM))
        except:
            status.add_error("Failed to write file: %s" % filename)
            csr = None
    return csr


# =======================================================================================================================
# Generate a private key and write to a file
# =======================================================================================================================
def _generate_private_key(status: process_status, filename: str, passphrase: str):
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )
        if passphrase == None:
            algorithm = serialization.NoEncryption()
        else:
            # Setup the encryption algorithm
            utf8_pass = passphrase.encode("utf-8")
            algorithm = serialization.BestAvailableEncryption(utf8_pass)
    except:
        private_key = None
    else:
        try:
            with open(filename, "wb") as keyfile:
                keyfile.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=algorithm,
                    )
                )
        except:
            errno, value = sys.exc_info()[:2]
            status.add_error(
                "Failed to write private key to an encrypted file with error: '%s' - '%s'" % (errno, value))
            status.add_error("Failed to write file: '%s'" % filename)
            private_key = None

    return private_key

# =======================================================================================================================
# Generate a self-signed public key.
# =======================================================================================================================
def _generate_public_key(status, private_key, filename, **kwargs):
    # Build info on the subject of the certificate
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, kwargs["country"]),
            x509.NameAttribute(
                NameOID.STATE_OR_PROVINCE_NAME, kwargs["state"]
            ),
            x509.NameAttribute(NameOID.LOCALITY_NAME, kwargs["locality"]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, kwargs["org"]),
            x509.NameAttribute(NameOID.COMMON_NAME, kwargs["hostname"]),
        ]
    )

    # Because this is self signed, the issuer is always the subject
    issuer = subject

    # This certificate is valid from now until 30 days
    valid_from = datetime.utcnow()
    valid_to = valid_from + timedelta(days=30)

    # Used to build the certificate
    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(valid_from)
        .not_valid_after(valid_to)
        .add_extension(x509.BasicConstraints(ca=True,
            path_length=None), critical=True)
    )
    try:
        # Sign the certificate with the private key
        public_key = builder.sign(
            private_key, hashes.SHA256(), default_backend()
        )
    except:
        status.add_error("Failed to sign certificate with the private key")
        public_key = None
    else:
        try:
            with open(filename, "wb") as certfile:
                certfile.write(public_key.public_bytes(serialization.Encoding.PEM))
        except:
            status.add_error("Failed to write public key to file: %s" % filename)
            public_key = None
    return public_key

# =======================================================================================================================
# Read a file and decrypt the content
# Decrypt the data using symetric encryption
# =======================================================================================================================
def protected_file_read(status, f_name, fernet_object):

    if not fernet_object:
        status.add_error("Missing password. Use the command 'set local password' to provide a password")
        list_data = None
        ret_val = process_status.Missing_password
    else:
        file_name = params.get_value_if_available(f_name)

        if not utils_io.is_path_exists(file_name):
            list_data = []       # new data file
            ret_val = process_status.SUCCESS
        else:
            ret_val, b_data = utils_io.read_protected_file(status, file_name)

            if not ret_val:
                try:
                    decrypt_data = fernet_object.decrypt(b_data)
                except:
                    status.add_error("Failed to decrypt data from file: %s" % file_name)
                    ret_val = process_status.ERR_process_failure
                    list_data = None
                else:
                    data_str = decrypt_data.decode()
                    list_data = str_to_list(data_str)
                    if not list_data:
                        status.add_error("Failed to decrypt data from file: %s" % file_name)
                        ret_val = process_status.ERR_process_failure
            else:
                list_data = None

    return [ret_val, list_data]

# =======================================================================================================================
# Protected file using a password
# Encrypt the data using symetric encryption
# =======================================================================================================================
def protected_file_write(status, f_name, list_data, fernet_object):

    if not fernet_object:
        status.add_error("Missing password. Use the command 'set local password' to provide a password")
        ret_val = process_status.Missing_password
    else:

        file_name = params.get_value_if_available(f_name)

        data = str(list_data)
        b_data = data.encode()

        try:
            encrypted = fernet_object.encrypt(b_data)
        except:
            status.add_error("Encryption of data written to file: '%s' failed" % file_name)
            ret_val = process_status.ERR_process_failure
        else:
            ret_val = utils_io.write_protected_file(status, file_name, encrypted)

    return ret_val
# =======================================================================================================================
# Fernet guarantees that a message encrypted using it cannot be manipulated or read without the key.
# Fernet is an implementation of symmetric authenticated cryptography.
# =======================================================================================================================
def generate_fernet(status, password, salt):

    password_arr = bytearray(password, 'utf-8')

    try:
        kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt = salt,
        iterations = 100000, backend=default_backend())

        key = base64.urlsafe_b64encode(kdf.derive(password_arr))
        f = Fernet(key)
    except:
        status.add_error("Failed to use encryption libraries")
        f = None

    return f
