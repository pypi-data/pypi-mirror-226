# coding=utf-8
# dd_license.py

# ------------------------------------------------------------------------------
# Copyright (C) 2017 EMC Corporation. All Rights Reserved.
# ------------------------------------------------------------------------------

"""
This module is used for installing license for Data Domain
"""
import common.log.logDeco as logDeco
import conf.dd_constants as dd_constants
import logging
import paramiko
import re
import time

"""
# dd_constants.py

# ------------------------------------------------------------------------------
#
# Copyright (C) 2017 DELL EMC Corporation. All Rights Reserved.
#
# ------------------------------------------------------------------------------

'''
Description: This module provides constant values for DD automation.

'''
import os
CONFDIR = os.path.dirname(os.path.abspath(__file__))

# prompt string
WAIT_FOR_PROMPT = 5

DDVE_OVA_DEPLOY_TIMEOUT = 10 * 60
DDVE_BOOT_TIME = 10 * 60
CONFIGURE_NETWORK = 'configure_network.sh'
PRIMARY_ETH = 'ethV0'
VERIFY_NETWORK = 'verify_network.sh'

DISK_NAME = 'dev3'
SLEEP_TIMEOUT = 10
DISK_BENCHMARK_TIMEOUT=350

DISK_SIZE = 200
DISK_BENCHMARK = {'cmd': 'disk benchmark start {0}\r',
                  'prompt': 'Are you sure? (yes|no|?) [no]: '}
SEND_YES = {'cmd': 'yes\r',
            'prompt': 'sysadmin@{0}# '}
ADD_STORAGE_TO_ACTIVE_TIER = {'cmd': 'storage add {0}\r',
                              'prompt': 'sysadmin@{0}# '}
CREATE_FILESYS = {'cmd': 'filesys create\r',
                  'prompt': 'Do you want to continue? (yes|no) [yes]: '}
ENABLE_FILESYS = {'cmd': 'filesys enable\r', 'prompt': 'sysadmin@{0}# '}
VERIFY_HARDWARE = {'cmd': 'disk show hardware\r', 'prompt': 'sysadmin@{0}# '}
VERIFY_FILESYS = {'cmd': 'filesys status\r', 'prompt': 'sysadmin@{0}# '}
DDBOOST_USER_CREATE = {'cmd': 'user add {0} role admin\r',
                       'prompt': 'Enter new password: '}
RE_ENTER_PASSWORD = {'cmd': '{0}\r', 'prompt': 'sysadmin@{0}# '}
SEND_RESPONSE = {'cmd': '{0}\r', 'prompt': 'Re-enter new password: '}
VERIFY_USER = {'cmd': 'user show list\r', 'prompt': 'sysadmin@{0}# '}
DDBOOST_ASSIGN = {'cmd': 'ddboost user assign {0}\r',
               'prompt': 'sysadmin@{0}# '}
DDBOOST_ASSIGN_VERIFY = {'cmd': 'ddboost user show\r',
               'prompt': 'sysadmin@{0}# '}
FILESYS_EXISTS = '**** A filesystem already exists.'
FILESYS_VERIFIED = 'The filesystem is enabled and running.'
LOCALHOST_PROMPT = 'sysadmin@localhost# '
VM_PROMPT = 'sysadmin@{0}# '
USER_EXISTS = '**** User "{0}" already exists.'
USER_DOES_NOT_EXIST = '**** The user "{0}" does not exist.'
DDBOOST_ENABLE = {'cmd': 'ddboost enable\r',
                  'prompt': 'sysadmin@{0}# '}
DDBOOST_STATUS = {'cmd': 'ddboost status\r',
                  'prompt': 'sysadmin@{0}# '}
DDBOOST_ENABLED = 'DD Boost enabled.'
DDBOOST_STATUS_ENABLED = 'DD Boost status: enabled'
DDBOOST_STATUS_DISABLED = 'DD Boost status: disabled'
USER_ADD_ERROR = '**** Error adding user "{0}".'
FILESYS_ENABLED = 'The filesystem is now enabled.'

# Install Data Domain License command
DD_INSTALL_LICENSE_TIMEOUT = 3 * 60
SET_SYSTEM_PASSPHRASE_TIMEOUT = 2 * 60
CTRL_D_CHAR = '\x04\x04'
CTRL_C_CHAR = '\x03\x03'
CARRIAGE_RETURN_CHAR = '\r'
DD_CHANGE_PSW_PROMPT = "Change the 'sysadmin' password at this time? (yes|no) [yes]: "
DD_CFG_SYS_PROMPT = 'Do you want to configure system using GUI wizard (yes|no) [no]: '
DD_CFG_NW_PROMPT = 'Configure Network at this time (yes|no) [no]: '
DD_LIC_CFG_PROPMT = 'Configure eLicenses at this time (yes|no) [no]: '
DD_CFG_SYS_CONFIRM_PROMPT = 'Configure System at this time (yes|no) [no]: '
DD_INITIAL_SETUP_PROMPTS = [
    DD_CHANGE_PSW_PROMPT,
    DD_CFG_SYS_PROMPT,
    DD_CFG_NW_PROMPT,
    DD_LIC_CFG_PROPMT,
    DD_CFG_SYS_CONFIRM_PROMPT
]
DD_VM_PROMPT_PATTERN = '{0}@.*#.*'
INSTALL_DD_LICENSE_CMD = "elicense update"
DD_SYS_PASSPHRASE = 'changeme'
SET_SYSTEM_PASSPHRASE_CMD = "system passphrase set"
ENTER_PASSPHRASE_PROMPT = 'Enter new passphrase: '
REENTER_PASSPHRASE_PROMPT = 'Re-enter new passphrase: '
PASSPHRASE_SET_MSG = 'The passphrase is set.'
ALREADY_SET_PASSPHRASE_TXT = 'passphrase is already set'

DD_LICENSE_CONTENT_PROMPT = 'Enter the content of license file and then press' \
                            ' Control-D, or press Control-C to cancel.'
DD_INSTALL_LICENSE_CONFIRM_PROMPT = 'Do you want to proceed? (yes|no) [yes]: '
DD_INSTALL_LICENSE_SUCCESS_MSG = 'eLicense(s) updated.'
DD_LICENSE_VERIFY_CMD = 'elicense show licenses'
DD_LICENSE_NOT_FOUND = 'No licenses found.'
DD_CAPACITY_LICENSE_FOUND = 'Capacity licenses'
DD_EMPTY_LICENSE_ERR = 'No licenses present'

# AD Integration commands
AUTHENTICATE_DC = {'cmd': 'authentication kerberos set realm {0} kdc-type {1} kdcs {2}\n',
                   'prompt': 'proceed? (yes|no) [no]: '}
ACCEPT_DC_AUTH = {'cmd': 'yes\n', 'prompt': 'Enter domain user (user or user@OTHERDOMAIN.COM): '}
DC_DOMAIN_USER = {'cmd': '{0}\n', 'prompt': 'Enter domain password: '}
DC_DOMAIN_PASSWORD = {'cmd': '{0}\n', 'prompt': '{0}'}

ADD_AD_GROUP = {'cmd': 'cifs local-group add "{0}" members "{1}"\n',
                'prompt': '{0}'}

DD_ADMIN_GROUP2_NAME = 'dd admin group2'
SET_DC_GROUP_TO_DD_ADMIN_GROUP = {'cmd': 'cifs option set "{0}" "{1}"\n',
                'prompt': '{0}'}
SET_DC_GROUP_RESULT = 'Set "{0}" to "{1}".'

VERIFY_DC_GROUP_TO_DD_ADMIN_GROUP_MAP = {'cmd': 'cifs option show\n',
                'prompt': '{0}'}

ADD_CIFS = {'cmd': 'adminaccess authentication add cifs\n',
            'prompt': '{0}'}

# check status of dc authenticate
DC_AUTH_STATUS = 'Failed to join realm'

# check status of group map
DC_GROUP_MAP_STATUS = 'Failed to add members: "{0}" is not a valid user or group'
DC_LOCAL_GROUP_STATUS = 'Failed to add members: Invalid group name:'

# verify AD Integration
# verify DC Authentication
VERIFY_DC_AUTH = {'cmd': 'authentication kerberos show config\n',
                  'prompt': '{0}'}
VERIFY_DC_AUTH_PATTERN = 'home realm:.*{0}.*kdc list.*{1}.*kdc type.*{2}'

# verify group mapping
VERIFY_GROUP_MAP = {'cmd': 'cifs local-group show detailed "{0}"\n',
                    'prompt': '{0}'}
VERIFY_GROUP_MAP_PATTERN = '{0}'

# verify cifs authentication
VERIFY_CIFS_AUTH = {'cmd': 'adminaccess authentication show\n',
                    'prompt': '{0}'}
VERIFY_CIFS_AUTH_PATTERN = 'CIFS authentication:.*enabled'.lower()

# paramiko timeout
PARAMIKO_TIMEOUT = 2*60
RECV_NBYTE = 4096

# dd local group
LOCAL_GROUP = 'BUILTIN\\administrators'

# DC OS type
DC_OS_TYPE = 'windows'
trap_host = 'snmp add trap-host {0}:{1} version v2c community public\r'
# SNMP config
SNMP_ADD_COMMUNITY = {'cmd': 'snmp add rw-community public hosts {0}\r',
                      'prompt': 'Confirm addition? (yes|no) [no]: '}
SNMP_ADD_TRAP_HOST = {'cmd': trap_host,
                      'prompt': 'sysadmin@{0}# '}
SNMP_CONFIG_VERIFY = {'cmd': 'snmp show config version v2c\r',
                      'prompt': 'sysadmin@{0}# '}
TRAP_HOST_EXISTS = 'Trap host, already exists.'
SNMP_ERROR = 'snmpd could not be enabled'
SNMP_OBJECT_EXISTS = 'The object already exists'
SNMP_NET_HOST_ADD = 'net hosts add {0} {1}'

# Addition of the DD as a backup target in AV
DD_TO_AV = 'mccli dd add --name={0}  --default-storage=true ' \
           '--user-name={1} --password={2} --password-confirm={2}' \
           '  --rw-community=public --trap-port=163 --snmp-port=161' \
           ' --max-streams=16'
VERIFY_ADD_DD_TO_VM = 'mccli dd show-prop --name={0}'

# HAU version check 
DATADOMAIN_VERSION = "system show version"

"""


def get_dd_license_content(dd_license_file_path):
    f = open(dd_license_file_path)
    return f.read()


@logDeco.logFunction
def install(dd_vm_details, dd_license_file_path):
    """Install or update the Data Domain license

        ddvm_details - DD VM informatoin (DICT)
            ip – DD VM IP Address (STRING)
            username - DD VM username (STRING)
            password - DD VM password (STRING)

        dd_license_file_path – absolute license file path (STRING)
        Return:
            install_status: (DICT)
                install_status['status'] = True/False(Boolean)
    """

    installation_status = {'status': False}
    try:
        logging.info('Installing DD License...')
        client = None
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(dd_vm_details['ip'],
                       username=dd_vm_details['username'],
                       password=dd_vm_details['password'])
        chan = client.invoke_shell()
        chan.settimeout(dd_constants.DD_INSTALL_LICENSE_TIMEOUT)

        install_cmd = dd_constants.INSTALL_DD_LICENSE_CMD
        logging.info('Executing command, %s', install_cmd)

        # Executing license update command
        dd_initial_setup_prompts = dd_constants.DD_INITIAL_SETUP_PROMPTS
        buff = ''
        dd_prompt_pattern = dd_constants.DD_VM_PROMPT_PATTERN.format(
            dd_vm_details['username'])
        while not re.search(dd_prompt_pattern, buff):
            resp = chan.recv(dd_constants.RECV_NBYTE)
            logging.debug(resp)

            if any(prompt in resp for prompt in dd_initial_setup_prompts):
                logging.debug('Found initial prompt, skipping...')
                time.sleep(1)
                chan.send('no')
                chan.send(dd_constants.CARRIAGE_RETURN_CHAR)

            time.sleep(1)
            buff += resp


        chan.send(install_cmd)
        chan.send(dd_constants.CARRIAGE_RETURN_CHAR)

        # Waiting for asking license content
        buff = ''
        while buff.find(dd_constants.DD_LICENSE_CONTENT_PROMPT) < 0:
            resp = chan.recv(dd_constants.RECV_NBYTE)
            logging.debug(resp)
            buff += resp

        # Passing the license content
        chan.send(dd_constants.CARRIAGE_RETURN_CHAR)
        chan.send(get_dd_license_content(dd_license_file_path))

        # Passing Ctrl + D
        chan.send(dd_constants.CTRL_D_CHAR)

        # Waiting for asking confirmation of license install
        buff = ""
        while not buff.endswith(
                dd_constants.DD_INSTALL_LICENSE_CONFIRM_PROMPT):
            resp = chan.recv(dd_constants.RECV_NBYTE)
            logging.debug(resp)
            if 'error' in resp or dd_constants.DD_EMPTY_LICENSE_ERR in resp:
                logging.error('Failed to install Data Domain license')
                return installation_status
            buff += resp

        # Passing yes to confirm the license installation
        chan.send('yes')
        chan.send(dd_constants.CARRIAGE_RETURN_CHAR)

        # Checking the status of install after return to prompt
        dd_prompt_pattern = dd_constants.DD_VM_PROMPT_PATTERN.format(
            dd_vm_details['username'])
        while not re.search(dd_prompt_pattern, buff):
            resp = chan.recv(dd_constants.RECV_NBYTE)
            logging.debug(resp)
            if dd_constants.DD_INSTALL_LICENSE_SUCCESS_MSG in resp:
                logging.info('Data Domain license installed successfully.')
                installation_status = {'status': True}
                return installation_status
            buff += resp

        logging.error('Failed to install Data Domain license')

    except Exception as err:
        logging.exception("Exception while installing DD license: %s",
                          str(err), exc_info=True)

    return installation_status


@logDeco.logFunction
def verify(dd_vm_details):
    """Verify the installation of Data Domain license

        ddvm_details - DD VM informatoin (DICT)
            ip – DD VM IP Address (STRING)
            username - DD VM username (STRING)
            password - DD VM password (STRING)

        Return:
            install_status: (DICT)
                install_status['status'] = True/False(Boolean)
    """

    installation_status = {'status': False}
    try:
        logging.info('Verifying DD License...')
        client = None
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(dd_vm_details['ip'],
                       username=dd_vm_details['username'],
                       password=dd_vm_details['password'])

        stdin, stdout, stderr = client.exec_command(
            dd_constants.DD_LICENSE_VERIFY_CMD)

        # sleep for 1 s to pass control to other thread
        while not stdout.channel.exit_status_ready():
            time.sleep(1)

        status = stdout.channel.recv_exit_status()

        capacity_lic_exists = False
        if status == 0:
            for line in stdout.readlines():
                logging.debug(line)
                if dd_constants.DD_LICENSE_NOT_FOUND in line:
                    logging.error(dd_constants.DD_LICENSE_NOT_FOUND)
                    return installation_status
                elif dd_constants.DD_CAPACITY_LICENSE_FOUND in line:
                    logging.info('Found license')
                    capacity_lic_exists = True

        else:
            logging.error('Failed to verify license, error: %s',
                          stderr.read())
            return installation_status

        if capacity_lic_exists:
            logging.info('Successfully verified license, status: installed')
            installation_status = {'status': True}
    except Exception as err:
        logging.exception("Exception while verifying DD license: %s",
                          str(err), exc_info=True)

    return installation_status


@logDeco.logFunction
def dd_first_time_user_login(dd_vm_details):
    """First time ssh login as sysadmin user to skip initial setup

        ddvm_details - DD VM information (DICT)
            ip – DD VM IP Address (STRING)
            username - DD VM username (STRING)
            password - DD VM password (STRING)

        Return:
            login_status: (DICT)
                login_status['status'] = True/False(Boolean)
    """

    login_status = {'status': False}
    try:
        logging.info('Logging into DD...')
        client = None
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(dd_vm_details['ip'],
                       username=dd_vm_details['username'],
                       password=dd_vm_details['password'])
        chan = client.invoke_shell()
        chan.settimeout(dd_constants.DD_INSTALL_LICENSE_TIMEOUT)

        verify_lic_cmd = dd_constants.DD_LICENSE_VERIFY_CMD
        logging.info('Executing command, %s', verify_lic_cmd)

        # Executing license update command
        chan.send(verify_lic_cmd)
        chan.send(dd_constants.CARRIAGE_RETURN_CHAR)

        dd_initial_setup_prompts = dd_constants.DD_INITIAL_SETUP_PROMPTS
        buff = ''
        # Checking the status of install after return to prompt
        dd_prompt_pattern = dd_constants.DD_VM_PROMPT_PATTERN.format(
            dd_vm_details['username'])
        while not re.search(dd_prompt_pattern, buff):
            resp = chan.recv(dd_constants.RECV_NBYTE)
            logging.debug(resp)

            if any(prompt in resp for prompt in dd_initial_setup_prompts):
                logging.debug('Found initial prompt, skipping...')
                time.sleep(1)
                chan.send('no')
                chan.send(dd_constants.CARRIAGE_RETURN_CHAR)

            time.sleep(1)
            buff += resp

        logging.info('Successfully logged into DD')
        login_status = {'status': True}
    except Exception as err:
        logging.error("Exception while login into DD: %s",
                      str(err), exc_info=True)

    return login_status