from pyVmomi import vim
from pyVim import connect
from pyVmomi import vim
#from conf import constants
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
ssl_context.verify_mode = ssl.CERT_NONE

HOST = '172.17.29.162'#constants.VCENTER_HOST
USER = 'administrator@vsphere.local'#constants.VCENTER_USER
PASSWORD = '12rmc*Help'#constants.VCENTER_PASSWORD
PORT = 443#constants.VCENTER_PORT
DATASTORE_NAME = 'datastore1'
VM_NAME = "test_vm2"

def wait_for_task(task):
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            print ('Task done')
            return task.info.result
        if task.info.state == 'error':
            print ('Task failed')
            task_done = True
            return task.info.error.msg

def connect_vcenter(host=HOST, username=USER, password=PASSWORD, port=PORT):
    print('connecting to vcenter...')
    service_instance = connect.SmartConnect(host=host,
                                            user=username,
                                            pwd=password,
                                            port=port,
                                            sslContext=ssl_context)
    print ('connected, vcenter: %s', service_instance)
    return service_instance


def find_network(network_name):
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.Network], True)
    networks = container.view
    for network in networks:
        print (network.name)
        if network_name == network.name:
            return network


def find_datastore(ds_name):
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.Datastore], True)
    datstores = container.view
    for ds in datstores:
        print (ds.name)
        if ds_name == ds.name:
            return ds

def find_vm(vm_name):
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.VirtualMachine], True)
    vms = container.view
    for vm in vms:
        print (vm.name)
        if vm_name == vm.name:
            return vm

VMX_PATH = []

def find_vmx(si, datacenter_obj, ds_obj, old_file_name, new_file_name):
    """
    function to copy a file in DS
    """
    dsbrowser = ds_obj.browser
    dsname = "[%s]" % ds_obj.summary.name
    search = vim.HostDatastoreBrowserSearchSpec()
    search.matchPattern = "*.vmx"
    search_ds = dsbrowser.SearchDatastoreSubFolders_Task(dsname, search)
    count =0
    while search_ds.info.state != "success":
       #print('Waiting....')
        count +=1
        if count > 150:
            break
        pass

    if search_ds.info.result:
        for rs in search_ds.info.result:
            print(rs.folderPath)
            for f in rs.file:
                if f.path == old_file_name:
                    print("Renaming....")
                    fileManager = si.content.fileManager
                    task = fileManager.CopyDatastoreFile_Task(sourceName=rs.folderPath + "/" + f.path,
                                                              sourceDatacenter=datacenter_obj,
                                                              destinationDatacenter=datacenter_obj,
                                                              destinationName=rs.folderPath + "/" + new_file_name,
                                                              force=True)
if __name__ == '__main__':
    si = connect_vcenter()

    content = si.RetrieveContent()
    datacenter = content.rootFolder.childEntity[0]
    ds = find_datastore('3PAR_VVOL1')
    find_vmx(si, datacenter, ds, 'New Virtual Machine.vmx', 'New Virtual Machine2.vmx')

    print('Rename request sent .')