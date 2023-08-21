from pyVim import connect
from pyVmomi import vim
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
ssl_context.verify_mode = ssl.CERT_NONE

HOST = "172.17.29.162"
USER = "administrator@vsphere.local"
PASSWORD = "Hpe@1234"
PORT = 443


def connect_vcenter(host=HOST, username=USER, password=PASSWORD, port=PORT):
    print('connecting to vcenter...')
    service_instance = connect.SmartConnect(host=host,
                                            user=username,
                                            pwd=password,
                                            port=port,
                                            sslContext=ssl_context)
    print('connected, vcenter: {} '.format(service_instance))
    return service_instance

connect_vcenter()
if __name__ == '__name__':
   connect_vcenter()