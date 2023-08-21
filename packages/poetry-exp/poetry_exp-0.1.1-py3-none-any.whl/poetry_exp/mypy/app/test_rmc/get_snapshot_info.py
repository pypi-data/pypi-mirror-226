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


def find_snapshot(snapshot_moref):
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.vm.Snapshot], True)
    vms = container.view
    for vm in vms:
        print (dir(vm))
        if snapshot_moref == vm.name:
            return vm


def list_snapshot(vm_name='vrb'):
   vm = find_vm(vm_name)
   if vm:
        print ('Found the VM')
        snap_info = vm.snapshot
        print (snap_info)
        snap_tree = snap_info.rootSnapshotList
        while snap_tree[0].childSnapshotList is not None:
            #print(snap_tree[0])
            print("Snap: Name: {0} => Description: {1}, id: {2}".format(
                snap_tree[0].name, snap_tree[0].description, snap_tree[0].id))
            if len(snap_tree[0].childSnapshotList) < 1:
                break
            snap_tree = snap_tree[0].childSnapshotList

   else:
        raise Exception('Cannot find the VM {}'.format(vm_name))


def find_vm_snapshot_by_name(vm_name, snapshot_name):
   vm = find_vm(vm_name)
   if vm:
        print ('Found the VM')
        snap_info = vm.snapshot
        #print (snap_info)
        snap_tree = snap_info.rootSnapshotList
        while snap_tree[0].childSnapshotList is not None:
            print("Snap: Name: {0} => Description: {1},".format(
                snap_tree[0].name, snap_tree[0].description))
            if snapshot_name == snap_tree[0].name:
                return snap_tree[0].snapshot
            if len(snap_tree[0].childSnapshotList) < 1:
                break
            snap_tree = snap_tree[0].childSnapshotList
   else:
        raise Exception('Cannot find the VM {}'.format(vm_name))


#https://pubs.vmware.com/vi3/sdk/ReferenceGuide/vim.vm.ConfigSpec.html
if __name__ == '__main__':
    #vm = find_vm('3par-vvol-vm3')
    # vm = list_snapshot('test-vm3')
    snapshot = find_vm_snapshot_by_name('test-vm3', 'RMCV_1571116340')
    print (snapshot)
    print(snapshot._moId)
    print(snapshot.config)

    #list_snapshot('test-vm3')