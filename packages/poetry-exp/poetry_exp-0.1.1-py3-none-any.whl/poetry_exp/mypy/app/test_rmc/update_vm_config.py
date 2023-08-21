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



def change_disk_path(vm_obj, path):
    """Change the disk mode on a virtual hard disk.
    :param si: Service Instance
    :param vm_obj: Virtual Machine Object
    :param disk_number: Disk number.
    :param mode: New disk mode.
    :param disk_prefix_label: Prefix name of disk.
    :return: True if success
    """
    #disk_label = disk_prefix_label + str(disk_number)
    virtual_disk_device = None

    # Find the disk device
    for dev in vm_obj.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualDisk):
            virtual_disk_device = dev

    virtual_disk_spec = vim.vm.device.VirtualDeviceSpec()
    virtual_disk_spec.operation = \
        vim.vm.device.VirtualDeviceSpec.Operation.edit
    virtual_disk_spec.device = virtual_disk_device
    #virtual_disk_spec.device.backing.diskMode = mode
    virtual_disk_spec.device.capacityInKB = 3 * 1024 * 1024
    virtual_disk_spec.device.backing.fileName = '[3PAR_VVOL1] naa.60002AC0000000000100BB4D0002107C/3par-vvol-vm5.vmdk'
    virtual_disk_spec.device.backing.backingObjectId = 'naa.60002AC0000000000100BBC50002107C'

    dev_changes = []
    dev_changes.append(virtual_disk_spec)
    spec = vim.vm.ConfigSpec()
    spec.deviceChange = dev_changes
    return spec


#https://pubs.vmware.com/vi3/sdk/ReferenceGuide/vim.vm.ConfigSpec.html
if __name__ == '__main__':
    #vm = find_vm('3par-vvol-vm3')
    vm = find_vm('aafak-vm1')
    print(vm.config)
    #spec = vim.VirtualMachineConfigSpec()
    vmx_file = vim.vm.FileInfo(logDirectory=None,
                               snapshotDirectory=None,
                               suspendDirectory=None,
                               vmPathName="[3PAR_VVOL1] naa.60002AC0000000000100BB4D0002107C/3par-vvol-vm4.vmx")

    # files = vm.config.files
    # #print(files)
    # files.vmPathName = "[3PAR_VVOL1] naa.60002AC0000000000100BB4D0002107C/3par-vvol-vm4.vmx"
    # #print(files.vmPathName)
    # spec = change_disk_path(vm, '')
    # spec.files = files
    # spec.vmPathName = "[3PAR_VVOL1] naa.60002AC0000000000100BB4D0002107C/3par-vvol-vm4.vmx"
    # spec.numCPUs = 2
    # print(spec)
    # vm.ReconfigVM_Task(spec)

    # print(type(vm.config))