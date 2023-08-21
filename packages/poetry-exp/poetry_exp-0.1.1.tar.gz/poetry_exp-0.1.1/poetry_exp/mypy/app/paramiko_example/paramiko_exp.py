"""
Paramiko is a Python implementation of the SSHv2 protocol, providing both client and server functionality.
While it leverages a Python C extension for low level cryptography (Cryptography),
Paramiko itself is a pure Python interface around SSH networking concepts.

pip install paramiko
"""

import paramiko
from paramiko import SSHClient


def exe_cmd(cmd, ip, username, password):
    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip, username, password)
    #ssh.connect('{}'.format(IP), port=xxx, username='xxx',password='xxx')

    stdin, stdout, stderr = ssh_client.exec_command(cmd)

    print('Ping switch: \n', stdout.readlines())


def exe_interactive_cmd(cmd, ip, username, password):
    import re, time
    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip, username, password)
    chan = ssh_client.invoke_shell()
    chan.settimeout(10)
    PROMPT_PATTERN = '{0}@.*#.*'.format('root')

    buff = ''
    while not re.search(PROMPT_PATTERN, buff):
        resp = chan.recv(4096)
        print resp
        time.sleep(1)
        buff += resp

    chan.send('date')
    chan.send('\r')

    buff = ''
    while buff.find(PROMPT_PATTERN) < 0:
        resp = chan.recv(4096)
        print(resp)
        buff += resp


if __name__ == '__main__':
    exe_cmd('ping -n 1 localhost\n', '127.0.0.1', '', '')