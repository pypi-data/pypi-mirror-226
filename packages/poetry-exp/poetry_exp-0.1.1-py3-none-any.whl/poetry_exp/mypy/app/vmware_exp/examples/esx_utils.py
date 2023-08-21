from pyVim import connect
from pyVmomi import vim
from app.vmware_exp.examples.conf import constants
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
ssl_context.verify_mode = ssl.CERT_NONE

HOST = constants.ESX_HOST
USER = constants.ESX_USER
PASSWORD = constants.ESX_PASSWORD
PORT = constants.ESX_PORT

HOST = "172.17.6.221"
USER = "root"
PASSWORD = "12esx*help"
PORT = constants.ESX_PORT


def connect_esx():
    print ('Connecting to ESXi host: ', HOST)
    si = connect.SmartConnect(
        host=HOST, user=USER, pwd=PASSWORD, port=PORT, sslContext=ssl_context)
    print(f'Connected to ESXi host, {si}')
    return si


def list_vswitches():
    vswitch_list = list()
    si = connect_esx()
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.HostSystem], True)
    hosts = container.view
    for host in hosts:
        print(host.__dict__)
        for vswitch in host.config.network.vswitch:
            print (vswitch.name)
            vswitch_list.append(vswitch)
    return vswitch_list


def list_port_group():
    portgroups = list()
    vswitch_list = list_vswitches()
    for vswitch in vswitch_list:
        for portgroup in vswitch.portgroup:
            print (portgroup)
            portgroups.append(portgroup)

    return portgroup



if __name__ == '__main__':
    #connect_esx()
    list_vswitches()
    #list_port_group()
