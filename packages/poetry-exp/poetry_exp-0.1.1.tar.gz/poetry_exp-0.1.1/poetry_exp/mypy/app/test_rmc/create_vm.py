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


si = connect_vcenter()
NETWORK = find_network("VM Network")


devices = []
datastore_path = '[' + DATASTORE_NAME + '] ' + VM_NAME
vmx_file = vim.vm.FileInfo(logDirectory=None,snapshotDirectory=None,suspendDirectory=None, vmPathName=datastore_path)


nicspec = vim.vm.device.VirtualDeviceSpec()
nicspec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
nic_type = vim.vm.device.VirtualVmxnet3()
nicspec.device = nic_type
nicspec.device.deviceInfo = vim.Description()
nicspec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
nicspec.device.backing.network = NETWORK
nicspec.device.backing.deviceName = NETWORK.name
nicspec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
nicspec.device.connectable.startConnected = True
nicspec.device.connectable.allowGuestControl = True
devices.append(nicspec)



scsi_ctr = vim.vm.device.VirtualDeviceSpec()
scsi_ctr.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
scsi_ctr.device = vim.vm.device.ParaVirtualSCSIController()
scsi_ctr.device.deviceInfo = vim.Description()
scsi_ctr.device.slotInfo = vim.vm.device.VirtualDevice.PciBusSlotInfo()
scsi_ctr.device.slotInfo.pciSlotNumber = 16
scsi_ctr.device.controllerKey = 100
scsi_ctr.device.unitNumber = 3
scsi_ctr.device.busNumber = 0
scsi_ctr.device.hotAddRemove = True
scsi_ctr.device.sharedBus = 'noSharing'
scsi_ctr.device.scsiCtlrUnitNumber = 7
devices.append(scsi_ctr)


unit_number = 0
sizeGB = 16
controller = scsi_ctr.device
disk_spec = vim.vm.device.VirtualDeviceSpec()
disk_spec.fileOperation = "create"
disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
disk_spec.device = vim.vm.device.VirtualDisk()
disk_spec.device.backing = vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
disk_spec.device.backing.diskMode = 'persistent'
disk_spec.device.backing.fileName = '[%s] %s/%s.vmdk' % ( DATASTORE_NAME, VM_NAME, VM_NAME )
disk_spec.device.unitNumber = unit_number
disk_spec.device.capacityInKB = sizeGB * 1024 * 1024
disk_spec.device.controllerKey = controller.key
devices.append(disk_spec)

content = si.RetrieveContent()
datacenter = content.rootFolder.childEntity[0]
vmfolder = datacenter.vmFolder
hosts = datacenter.hostFolder.childEntity
resource_pool = hosts[0].resourcePool
config = vim.vm.ConfigSpec(name=VM_NAME, memoryMB=1024, numCPUs=2, files=vmx_file, guestId='ubuntu64Guest', version='vmx-09', deviceChange=devices)
task = vmfolder.CreateVM_Task(config=config, pool=resource_pool)
wait_for_task(task)