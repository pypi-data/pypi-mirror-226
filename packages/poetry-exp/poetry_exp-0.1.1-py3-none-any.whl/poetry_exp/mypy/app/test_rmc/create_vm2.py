from pyVmomi import vim
from pyVim import connect
from pyVmomi import vim
#from conf import constants
import ssl
import logging
from test_rmc import rmv_utils
LOG = logging.getLogger(__name__)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
ssl_context.verify_mode = ssl.CERT_NONE

HOST = '172.17.29.162'#constants.VCENTER_HOST
USER = 'administrator@vsphere.local'#constants.VCENTER_USER
PASSWORD = '12rmc*Help'#constants.VCENTER_PASSWORD
PORT = 443#constants.VCENTER_PORT
DATASTORE_NAME = 'datastore1'
VM_NAME = "test_vm23"

def wait_for_task(task):
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            print ('Task done')
            return task.info.result
        if task.info.state == 'error':
            print ('Task failed')
            task_done = True
            print (task.info.error.msg)
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

#si = connect_vcenter()

def find_network(network_name):
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
    datastores = container.view
    for datastore in datastores:
        #print (datastore._GetMoId)
        if ds_name == datastore.name:
            print('Found DS')
            return datastore
#NETWORK = find_network("VM Network")






def buildSpec_for_VM_ConfigInfo(vmname, datastore, ds_moref, prop_dict, is_reconfigure=False):
    try:

        LOG.info("buildSpec_for_VM_ConfigInfo :Enter")
        LOG.info('VM Configuration: {0}'.format(prop_dict))

        datastore_path = '[' + datastore + '] ' + vmname
        vmx_file = vim.vm.FileInfo(logDirectory=None, snapshotDirectory=None, suspendDirectory=None,
                                   vmPathName=datastore_path)

        spec = vim.vm.ConfigSpec()
        spec.name = vmname
        spec.files = vmx_file
        virtualDeviceConfig_Spec_list = []

        hw = prop_dict['hardware']

        i = 0
        count = 0
        deviceKey = []

        for i in range(len(hw)):
            for hkeys in hw[i]:
                print('...............' + str(hw[i][hkeys]))

                if rmv_utils.VMWARE_VM_VIRTUAL_LSILOGIC_CONTROLLER == hkeys:
                    try:
                        virtDeviceScsiCont = vim.vm.device.VirtualDeviceSpec()
                        virtDeviceScsiCont.device = vim.vm.device.VirtualLsiLogicController()
                        virtDeviceScsiCont.device.key = hw[i][hkeys].get('key', None)
                        devInfo = hw[i][hkeys].get('deviceInfo', None)
                        virtDeviceScsiCont.device.deviceInfo = vim.Description()
                        virtDeviceScsiCont.device.deviceInfo.summary = devInfo.get('summary', None)
                        virtDeviceScsiCont.device.deviceInfo.label = devInfo.get('label', None)
                        virtDeviceScsiCont.device.controllerKey = hw[i][hkeys].get('controllerKey', None)
                        virtDeviceScsiCont.device.unitNumber = hw[i][hkeys].get('unitNumber', None)
                        virtDeviceScsiCont.device.busNumber = hw[i][hkeys].get('busNumber', None)

                        virtDeviceScsiCont.device.sharedBus = hw[i][hkeys].get('sharedBus', None)
                        deviceKey.append(virtDeviceScsiCont.device.key)
                        if is_reconfigure == False:
                            virtDeviceScsiCont.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

                        virtualDeviceConfig_Spec_list.append(virtDeviceScsiCont)
                        #print('...........virtDeviceScsiCont '+str(virtDeviceScsiCont))
                    except Exception as e:
                        #LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        LOG.exception(e)
                        #msg = _("Found error in collecting config properties of LSI Logic Controller")
                        #LOG.info(msg)
                        #raise msg
                        print('Eror: '+str(e))

                elif rmv_utils.VMWARE_VM_VIRTUAL_LSILOGIC_SAS_CONTROLLER == hkeys:
                    try:
                        virtLsiLogicSASCont = vim.vm.device.VirtualDeviceSpec()
                        virtLsiLogicSASCont.device = vim.vm.device.VirtualLsiLogicController()

                        virtLsiLogicSASCont.device.key = hw[i][hkeys].get('key', None)
                        devInfo = hw[i][hkeys].get('deviceInfo', None)
                        virtLsiLogicSASCont.device.deviceInfo = vim.Description()
                        virtLsiLogicSASCont.device.deviceInfo.label = devInfo.get('label', None)
                        virtLsiLogicSASCont.device.deviceInfo.summary = devInfo.get('summary', None)
                        virtLsiLogicSASCont.device.controllerKey = hw[i][hkeys].get('controllerKey', None)
                        virtLsiLogicSASCont.device.unitNumber = hw[i][hkeys].get('unitNumber', None)
                        virtLsiLogicSASCont.device.busNumber = hw[i][hkeys].get('busNumber', None)
                        virtLsiLogicSASCont.device.sharedBus = hw[i][hkeys].get('sharedBus', None)
                        deviceKey.append(virtLsiLogicSASCont.device.key)
                        if is_reconfigure == False:
                            virtLsiLogicSASCont.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

                        virtualDeviceConfig_Spec_list.append(virtLsiLogicSASCont)
                        #print ('..........virtLsiLogicSASCont: '+str(virtLsiLogicSASCont))
                    except Exception as e:
                        #LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        LOG.exception(e)
                        print(e)
                        #msg = _("Found error in collecting config properties of LSI Logic SAS Controller")
                        #LOG.info(msg)
                        #raise msg

                elif rmv_utils.VMWARE_VM_VIRTUAL_PARA_LSILOGIC_CONTROLLER == hkeys:
                    try:
                        paraVirtScsiCont = vim.vm.device.VirtualDeviceSpec()
                        paraVirtScsiCont.device = vim.vm.device.ParaVirtualSCSIController()

                        paraVirtScsiCont.device.key = hw[i][hkeys].get('key', None)
                        devInfo = hw[i][hkeys].get('deviceInfo', None)
                        paraVirtScsiCont.device.deviceInfo = vim.Description()
                        paraVirtScsiCont.device.deviceInfo.label = devInfo.get('label', None)
                        paraVirtScsiCont.device.deviceInfo.summary = devInfo.get('summary', None)
                        paraVirtScsiCont.device.controllerKey = hw[i][hkeys].get('controllerKey', None)
                        paraVirtScsiCont.device.unitNumber = hw[i][hkeys].get('unitNumber', None)
                        paraVirtScsiCont.device.busNumber = hw[i][hkeys].get('busNumber', None)
                        paraVirtScsiCont.device.sharedBus = hw[i][hkeys].get('sharedBus', None)
                        deviceKey.append(paraVirtScsiCont.device.key)
                        if is_reconfigure == False:
                            paraVirtScsiCont.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

                        virtualDeviceConfig_Spec_list.append(paraVirtScsiCont)
                        #print('..........paraVirtScsiCont: ' + str(paraVirtScsiCont))
                    except Exception as e:
                        LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        LOG.exception(e)
                        msg = _("Found error in collecting config properties of PARA LSI Logic Controller")
                        LOG.info(msg)
                        raise msg

                elif rmv_utils.VMWARE_VM_VIRTUAL_DISK == hkeys:
                    try:
                        count = count + 1
                        VirtualDiskFlatVer2BackingInfo = vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
                        if count == 1:
                            VirtualDiskFlatVer2BackingInfo.fileName = "[" + datastore + "]" + " " + vmname + "/" + vmname + ".vmdk"
                        elif count > 1:
                            VirtualDiskFlatVer2BackingInfo.fileName = "[" + datastore + "]" + " " + vmname + "/" + vmname + "_" + str(
                                count) + ".vmdk"

                        backing = hw[i][hkeys].get('backing', None)
                        VirtualDiskFlatVer2BackingInfo.diskMode = backing.get('diskMode', None)
                        VirtualDiskFlatVer2BackingInfo.datastore = find_datastore(datastore)

                        VirtualDisk = vim.vm.device.VirtualDisk()
                        devInfo = hw[i][hkeys].get('deviceInfo', None)
                        VirtualDisk.deviceInfo = vim.Description()
                        VirtualDisk.deviceInfo.label = devInfo.get('label', None)
                        VirtualDisk.deviceInfo.summary = devInfo.get('summary', None)
                        VirtualDisk.controllerKey = hw[i][hkeys].get('controllerKey', None)
                        VirtualDisk.key = hw[i][hkeys].get('key', None)
                        VirtualDisk.unitNumber = hw[i][hkeys].get('unitNumber', None)
                        VirtualDisk.capacityInKB = hw[i][hkeys].get('capacityInKB', None)
                        VirtualDisk.backing = VirtualDiskFlatVer2BackingInfo
                        deviceKey.append(VirtualDisk.key)
                        VirtualDeviceConfigSpecVD = vim.vm.device.VirtualDeviceSpec()
                        if is_reconfigure == False:
                            VirtualDeviceConfigSpecVD.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
                            VirtualDeviceConfigSpecVD.fileOperation = vim.VirtualDeviceConfigSpecFileOperation.create

                        VirtualDeviceConfigSpecVD.device = VirtualDisk
                        virtualDeviceConfig_Spec_list.append(VirtualDeviceConfigSpecVD)

                       # print('..........VirtualDeviceConfigSpecVD: ' + str(VirtualDeviceConfigSpecVD))
                    except Exception as e:
                        #LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        LOG.exception(e)
                        print(e)
                        #msg = _("Found error in collecting config properties of Virtual Disk Information")
                        #LOG.info(msg)
                        #raise msg

                elif rmv_utils.VMWARE_VM_NETWORK_E100 == hkeys:
                    try:
                        virtDeviceNW = vim.vm.device.VirtualDeviceSpec()
                        virtDeviceNW.device = vim.vm.device.VirtualE1000()
                        devInfo = hw[i][hkeys].get('deviceInfo', None)
                        virtDeviceNW.device.deviceInfo = vim.Description()
                        virtDeviceNW.device.deviceInfo.label = devInfo.get('label', None)
                        virtDeviceNW.device.deviceInfo.summary = devInfo.get('summary', None)
                        virtDeviceNW.device.key = hw[i][hkeys].get('key', None)
                        virtDeviceNW.device.addressType = "generated"
                        virtDeviceNW.device.controllerKey = hw[i][hkeys].get('controllerKey', None)
                        virtDeviceNW.device.unitNumber = hw[i][hkeys].get('unitNumber', None)
                        # VirtualEthernetCardNetworkBackingInfo = client_factory.create('ns0:VirtualEthernetCardNetworkBackingInfo')
                        backing = hw[i][hkeys].get('backing', None)
                        print ('comes here...................')
                        get_network_backing_info(backing, virtDeviceNW.device)
                        deviceKey.append(virtDeviceNW.device.key)

                        if is_reconfigure == False:
                            virtDeviceNW.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

                        virtualDeviceConfig_Spec_list.append(virtDeviceNW)
                    except Exception as e:
                        #LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        #LOG.exception(e)
                        #msg = _("Found error in collecting config properties of Network")
                        #LOG.info(msg)
                        #raise msg
                        print(e)
                        raise e

                elif rmv_utils.VMWARE_VM_NETWORK_VMXNET in hkeys:
                    try:
                        virtDeviceNW = vim.vm.device.VirtualDeviceSpec()
                        virtDeviceNW.device = vim.vm.device.VirtualVmxnet()
                        if hkeys.endswith("2"):
                            virtDeviceNW.device = vim.vm.device.VirtualVmxnet2()
                        elif hkeys.endswith("3"):
                            virtDeviceNW.device = vim.vm.device.VirtualVmxnet3()

                        devInfo = hw[i][hkeys].get('deviceInfo', None)
                        virtDeviceNW.device.deviceInfo = vim.Description()
                        virtDeviceNW.device.deviceInfo.label = devInfo.get('label', None)
                        virtDeviceNW.device.deviceInfo.summary = devInfo.get('summary', None)
                        virtDeviceNW.device.key = hw[i][hkeys].get('key', None)
                        virtDeviceNW.device.addressType = "generated"
                        virtDeviceNW.device.controllerKey = hw[i][hkeys].get('controllerKey', None)
                        virtDeviceNW.device.unitNumber = hw[i][hkeys].get('unitNumber', None)

                        backing = hw[i][hkeys].get('backing', None)
                        get_network_backing_info(backing, virtDeviceNW.device)

                        deviceKey.append(virtDeviceNW.device.key)
                        if is_reconfigure == False:
                            virtDeviceNW.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

                        virtualDeviceConfig_Spec_list.append(virtDeviceNW)
                    except Exception as e:
                        # LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        # LOG.exception(e)
                        # msg = _("Found error in collecting config properties of VMX Network")
                        # LOG.info(msg)
                        # raise msg
                        print(e)
                        raise e


                elif rmv_utils.VMWARE_VM_NETWORK_PCNET_32 == hkeys:
                    try:
                        virtDeviceNW = vim.vm.device.VirtualDeviceSpec()
                        virtDeviceNW.device = vim.vm.device.VirtualPCNet32()

                        devInfo = hw[i][hkeys].get('deviceInfo', None)
                        virtDeviceNW.device.deviceInfo = vim.Description()
                        virtDeviceNW.device.deviceInfo.label = devInfo.get('label', None)
                        virtDeviceNW.device.deviceInfo.summary = devInfo.get('summary', None)
                        virtDeviceNW.device.key = hw[i][hkeys].get('key', None)
                        virtDeviceNW.device.addressType = "generated"
                        virtDeviceNW.device.controllerKey = hw[i][hkeys].get('controllerKey', None)
                        virtDeviceNW.device.unitNumber = hw[i][hkeys].get('unitNumber', None)

                        backing = hw[i][hkeys].get('backing', None)
                        get_network_backing_info(backing, virtDeviceNW.device)

                        deviceKey.append(virtDeviceNW.device .key)
                        if is_reconfigure == False:
                            virtDeviceNW.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

                        virtualDeviceConfig_Spec_list.append(virtDeviceNW)
                    except Exception as e:
                        # LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        # LOG.exception(e)
                        # msg = _("Found error in collecting config properties of Network PCNET")
                        # LOG.info(msg)
                        # raise msg
                        raise e

                elif rmv_utils.VMWARE_VM_VIRTUAL_AHCI_CONTROLLER == hkeys:
                    try:
                        virtAHCICont = vim.vm.device.VirtualDeviceSpec()
                        virtAHCICont.device = vim.vm.device.VirtualAHCIController()
                        virtAHCICont.device.key = hw[i][hkeys].get('key', None)
                        devInfo = hw[i][hkeys].get('deviceInfo', None)
                        virtAHCICont.device.deviceInfo = vim.Description()
                        virtAHCICont.device.deviceInfo.label = devInfo.get('label', None)
                        virtAHCICont.device.deviceInfo.summary = devInfo.get('summary', None)
                        virtAHCICont.device.controllerKey = hw[i][hkeys].get('controllerKey', None)
                        virtAHCICont.device.unitNumber = hw[i][hkeys].get('unitNumber', None)
                        virtAHCICont.device.busNumber = hw[i][hkeys].get('busNumber', None)
                        virtAHCICont.device.device = hw[i][hkeys].get('device', None)
                        deviceKey.append(virtAHCICont.device.key)
                        if is_reconfigure == False:
                            virtAHCICont.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

                        virtualDeviceConfig_Spec_list.append(virtAHCICont)
                        #print('..........virtAHCICont: ' + str(virtAHCICont))
                    except Exception as e:
                        LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        LOG.exception(e)
                        msg = _("Found error in collecting config properties of AHCI Controller")
                        LOG.info(msg)
                        continue

                elif rmv_utils.VMWARE_VM_VIRTUAL_CDROM == hkeys:
                    try:
                        VirtualDeviceConnectInfo = vim.VirtualDeviceConnectInfo()
                        virtDeviceCD = vim.vm.device.VirtualDeviceSpec()
                        virtDeviceCD.device = vim.vm.device.VirtualCdrom()
                        devInfo = hw[i][hkeys].get('deviceInfo', None)
                        virtDeviceCD.device.key = hw[i][hkeys].get('key', None)
                        virtDeviceCD.device.deviceInfo = vim.Description()
                        virtDeviceCD.device.deviceInfo.label = devInfo.get('label', None)
                        virtDeviceCD.device.deviceInfo.summary = devInfo.get('summary', None)
                        connectable = hw[i][hkeys]['connectable']
                        if connectable:
                            VirtualDeviceConnectInfo.startConnected = connectable.get('startConnected', None)
                            VirtualDeviceConnectInfo.allowGuestControl = connectable.get('allowGuestControl', None)
                            VirtualDeviceConnectInfo.status = connectable.get('status', None)
                            VirtualDeviceConnectInfo.connected = connectable.get('connected', None)
                        virtDeviceCD.device.connectable = VirtualDeviceConnectInfo
                        deviceKey.append(virtDeviceCD.device.key)
                        VirtualCdromRemoteAtapiBackingInfo = vim.vm.device.VirtualCdrom.RemoteAtapiBackingInfo()
                        backing = hw[i][hkeys].get('backing', None)
                        if backing:
                            if 'deviceName' in hw[i][hkeys]['backing']:
                                VirtualCdromRemoteAtapiBackingInfo.deviceName = backing.get('deviceName', None)
                            else:
                                VirtualCdromRemoteAtapiBackingInfo.deviceName = " "

                            if 'useAutoDetect' in hw[i][hkeys]['backing']:
                                VirtualCdromRemoteAtapiBackingInfo.useAutoDetect = backing.get('useAutoDetect')
                            else:
                                VirtualCdromRemoteAtapiBackingInfo.useAutoDetect = False

                            if VirtualCdromRemoteAtapiBackingInfo.deviceName == None:
                                VirtualCdromRemoteAtapiBackingInfo.deviceName = " "

                        virtDeviceCD.device.backing = VirtualCdromRemoteAtapiBackingInfo

                        virtDeviceCD.device.controllerKey = hw[i][hkeys].get('controllerKey', None)
                        virtDeviceCD.device.unitNumber = hw[i][hkeys].get('unitNumber', None)

                        if is_reconfigure == False:
                            virtDeviceCD.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

                        virtualDeviceConfig_Spec_list.append(virtDeviceCD)
                        #print('............virtDeviceCD'+str(virtDeviceCD))
                    except Exception as e:
                        # LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        # LOG.exception(e)
                        # msg = _("Found error in collecting config properties of CDROM")
                        # LOG.info(msg)
                        # raise (msg)
                        raise e

                elif rmv_utils.VMWARE_VM_VIRTUAL_FLOPPY == hkeys:
                    try:
                        virtDeviceFP = vim.vm.device.VirtualDeviceSpec()
                        virtDeviceFP.device = vim.vm.device.VirtualFloppy()
                        VirtualDeviceConnectInfo =  vim.VirtualDeviceConnectInfo()
                        devInfo = hw[i][hkeys].get('deviceInfo', None)
                        virtDeviceFP.device.key = hw[i][hkeys].get('key', None)
                        virtDeviceFP.device.deviceInfo = vim.Description()
                        virtDeviceFP.device.deviceInfo.label = devInfo.get('label', None)
                        virtDeviceFP.device.deviceInfo.summary = devInfo.get('summary', None)
                        connectable = hw[i][hkeys]['connectable']
                        if connectable:
                            VirtualDeviceConnectInfo.startConnected = connectable.get('startConnected', None)
                            VirtualDeviceConnectInfo.allowGuestControl = connectable.get('allowGuestControl', None)
                            VirtualDeviceConnectInfo.status = connectable.get('status', None)
                            VirtualDeviceConnectInfo.connected = connectable.get('connected', None)
                        virtDeviceFP.device.connectable = VirtualDeviceConnectInfo
                        deviceKey.append(virtDeviceFP.device.key)
                        VirtualFPRemoteAtapiBackingInfo = vim.vm.device.VirtualFloppy.RemoteDeviceBackingInfo()
                        backing = hw[i][hkeys].get('backing', None)
                        if backing:
                            if 'deviceName' in hw[i][hkeys]['backing']:
                                VirtualFPRemoteAtapiBackingInfo.deviceName = hw[i][hkeys]['backing']['deviceName']

                            else:
                                VirtualFPRemoteAtapiBackingInfo.deviceName = " "

                            if 'useAutoDetect' in hw[i][hkeys]['backing']:
                                VirtualFPRemoteAtapiBackingInfo.useAutoDetect = hw[i][hkeys]['backing']['useAutoDetect']
                            else:
                                VirtualFPRemoteAtapiBackingInfo.useAutoDetect = False

                            if VirtualFPRemoteAtapiBackingInfo.deviceName == None:
                                VirtualFPRemoteAtapiBackingInfo.deviceName = " "

                        virtDeviceFP.device.backing = VirtualFPRemoteAtapiBackingInfo

                        virtDeviceFP.device.controllerKey = hw[i][hkeys].get('controllerKey', None)
                        virtDeviceFP.device.unitNumber = hw[i][hkeys].get('unitNumber', None)

                        if is_reconfigure == False:
                            virtDeviceFP.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

                        virtualDeviceConfig_Spec_list.append(virtDeviceFP)
                        #print('.................virtDeviceFP '+ str(virtDeviceFP))
                    except Exception as e:
                        # LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        # LOG.exception(e)
                        # msg = _("Found error in collecting config properties of Floppy")
                        # LOG.info(msg)
                        # raise (msg)
                        raise e


        spec.deviceChange = virtualDeviceConfig_Spec_list

        for ckeys in prop_dict:
            if ckeys == 'memoryMB':
                spec.memoryMB = prop_dict['memoryMB']
            elif ckeys == 'numCPU':
                spec.numCPUs = prop_dict['numCPU']
            elif ckeys == 'numCoresPerSocket':
                spec.numCoresPerSocket = prop_dict['numCoresPerSocket']
            elif ckeys == 'virtualICH7MPresent':
                spec.virtualICH7MPresent = prop_dict['virtualICH7MPresent']
            elif ckeys == 'virtualSMCPresent':
                spec.virtualSMCPresent = prop_dict['virtualSMCPresent']
            elif ckeys == 'defaultPowerOps':
                power_option = vim.vm.DefaultPowerOpInfo()
                # TODo need to check what option provided in keys, prop_dict['defaultPowerOps']
                spec.powerOpInfo = power_option
            elif ckeys == 'bootOptions':
                bootOpt = vim.VirtualMachineBootOptions()
                for bkeys in prop_dict['bootOptions']:
                    if bkeys == 'bootDelay':
                        bootOpt.bootDelay = prop_dict['bootOptions']['bootDelay']
                    elif bkeys == 'enterBIOSSetup':
                        bootOpt.enterBIOSSetup = prop_dict['bootOptions']['enterBIOSSetup']
                    elif bkeys == 'bootRetryEnabled':
                        bootOpt.bootRetryEnabled = prop_dict['bootOptions']['bootRetryEnabled']
                    elif bkeys == 'bootRetryDelay':
                        bootOpt.bootRetryDelay = prop_dict['bootOptions']['bootRetryDelay']
                    elif bkeys == 'networkBootProtocol':
                        bootOpt.networkBootProtocol = prop_dict['bootOptions']['networkBootProtocol']
                if 'bootOrder' in prop_dict['bootOptions']:
                    # ToDo Need to check  prop_dict['bootOptions']['bootOrder']
                    bootOpt.bootOrder = [vim.vm.BootOptions.BootableDevice()]
                else:
                    LOG.info('device key: {0}'.format(deviceKey))
                    # ToDo Need to check bootOpt.bootOrder=deviceKey
                    bootOpt.bootOrder = [vim.vm.BootOptions.BootableDevice()]#[vim.vm.BootOptions.BootableCdromDevice()]
                spec.bootOptions = bootOpt
            elif ckeys == 'tools':
                tool = vim.vm.ToolsConfigInfo()
                # ToDo Need to check what value to set
                spec.tools = tool
            elif ckeys == 'flags':
                flag = vim.vm.FlagInfo()
                # ToDo Need to check what value to set
                spec.flags = flag

            elif ckeys == 'guestId':
                spec.guestId = prop_dict['guestId']
            elif ckeys == 'alternateGuestName':
                spec.alternateGuestName = prop_dict['alternateGuestName']
            elif ckeys == 'annotation':
                spec.annotation = prop_dict['annotation']
            elif ckeys == 'version':
                spec.version = prop_dict['version']
            elif ckeys == 'memoryHotAddEnabled':
                spec.memoryHotAddEnabled = prop_dict['memoryHotAddEnabled']
            elif ckeys == 'cpuHotAddEnabled':
                spec.cpuHotAddEnabled = prop_dict['cpuHotAddEnabled']
            elif ckeys == 'changeVersion':
                spec.changeVersion = prop_dict['changeVersion']
            elif ckeys == 'cpuAllocation':
                sharesLevel = vim.SharesLevel()
                sharesLevel.value = prop_dict['cpuAllocation']['shares']['level']
                sharesInfo = vim.SharesInfo()
                sharesInfo.shares = prop_dict['cpuAllocation']['shares']['shares']
                resourceAllocationSpec = vim.ResourceAllocationInfo()
                resourceAllocationSpec.reservation = prop_dict['cpuAllocation']['reservation']
                resourceAllocationSpec.limit = prop_dict['cpuAllocation']['limit']
                resourceAllocationSpec.expandableReservation = prop_dict['cpuAllocation']['expandableReservation']
                sharesInfo.level = vim.SharesInfo.Level(prop_dict['memoryAllocation']['shares']['level'])
                resourceAllocationSpec.shares = sharesInfo
                spec.cpuAllocation = resourceAllocationSpec
            elif ckeys == 'cpuHotRemoveEnabled':
                spec.cpuHotRemoveEnabled = prop_dict['cpuHotRemoveEnabled']
            elif ckeys == 'guestAutoLockEnabled':
                spec.guestAutoLockEnabled = prop_dict['guestAutoLockEnabled']
            elif ckeys == 'maxMksConnections':
                spec.maxMksConnections = prop_dict['maxMksConnections']
            elif ckeys == 'memoryAllocation':
                sharesLevel = vim.SharesLevel()
                sharesLevel.value = prop_dict['memoryAllocation']['shares']['level']
                sharesInfo = vim.SharesInfo()
                sharesInfo.shares = prop_dict['memoryAllocation']['shares']['shares']
                resourceAllocationSpec = vim.ResourceAllocationInfo()
                resourceAllocationSpec.reservation = prop_dict['memoryAllocation']['reservation']
                resourceAllocationSpec.limit = prop_dict['memoryAllocation']['limit']
                resourceAllocationSpec.expandableReservation = prop_dict['memoryAllocation']['expandableReservation']
                sharesInfo.level = vim.SharesInfo.Level(prop_dict['memoryAllocation']['shares']['level'])
                resourceAllocationSpec.shares = sharesInfo
                spec.memoryAllocation = resourceAllocationSpec
            elif ckeys == 'memoryReservationLockedToMax':
                spec.memoryReservationLockedToMax = prop_dict['memoryReservationLockedToMax']
            elif ckeys == 'npivTemporaryDisabled':
                spec.npivTemporaryDisabled = prop_dict['npivTemporaryDisabled']
            elif ckeys == 'vAssertsEnabled':
                spec.vAssertsEnabled = prop_dict['vAssertsEnabled']
            elif ckeys == 'swapPlacement':
                spec.swapPlacement = prop_dict['swapPlacement']
            elif ckeys == 'firmware':
                spec.firmware = prop_dict['firmware']
            elif ckeys == 'extraConfig' and is_reconfigure == False:
                # Todo Need to check what is coming in prop_dict['extraConfig']
                extra_configs = []
                for key, value in prop_dict['extraConfig'].items():
                    option = vim.option.OptionValue()
                    option.key = key
                    option.value = value
                    extra_configs.append(option)
                spec.extraConfig = extra_configs

        LOG.info("buildSpec_for_VM_ConfigInfo :Exit")
        print('spec: {0}'.format(spec))
        return spec

    except Exception as e:
        msg = "ConfigInfo preparation failed for Express protect operation"
        if hasattr(e, "msg"):
            LOG.error(('%s'), e.msg)
        LOG.exception("Exception: %s", e)
        raise e(msg=msg)


def get_network_backing_info(backing, VirtualDeviceConfigSpecNW):
    LOG.info("Get network backing info : Enter")
    network = backing.get('network', None)
    ports = backing.get('port', None)
    if network:
        LOG.info("Creating a vSwitch Ethernet Card object")
        VirtualEthernetCardNetworkBackingInfo = vim.VirtualEthernetCardNetworkBackingInfo()

        VirtualEthernetCardNetworkBackingInfo.deviceName = backing.get('deviceName', None)
        VirtualEthernetCardNetworkBackingInfo.network = vim.Network(network.get('value', None))
        #VirtualEthernetCardNetworkBackingInfo.network.value = network.get('value', None)
        #VirtualEthernetCardNetworkBackingInfo.network._type = network.get('_type', None)
        VirtualEthernetCardNetworkBackingInfo.useAutoDetect = backing.get('useAutoDetect', None)
        VirtualDeviceConfigSpecNW.backing = VirtualEthernetCardNetworkBackingInfo
    elif ports:
        LOG.info("Creating a dSwitch virtual port object")
        VirtualEthernetCardDistributedVirtualPortBackingInfo = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
        VirtualEthernetCardDistributedVirtualPortBackingInfo.port = vim.dvs.PortConnection()
        VirtualEthernetCardDistributedVirtualPortBackingInfo.port.switchUuid = ports.get('switchUuid', None)
        VirtualDeviceConfigSpecNW.backing = VirtualEthernetCardDistributedVirtualPortBackingInfo
    LOG.info("Get network backing info : Exit")

    def recreate_VM(self, vm_spec, vmname, ds_moref, resPool, host_ref):
        try:
            LOG.info("recreateVM :Enter")
            res_moref = vim.get_moref(resPool,"ResourcePool")

            ds_moref_obj = vim.get_moref(ds_moref, "Datastore")
            #Changes to access the corresponding datacenter using datastores
            dc_ref = self.get_parent_datacenter(ds_moref_obj)

            LOG.info("Calling recreateVM_Task ")
            ret = self.vmops_obj.CreateVM_Task(dc_ref.value, vm_spec, res_moref, host_ref)
            vm_moref = vm_util.get_vm_ref_from_name(self._session, vmname)
        except Exception as e:
            msg = "Recreate VM failed for Express protect operation"
            if hasattr(e, "msg"):
                LOG.error(('%s'), e.msg)
            LOG.exception("Exception: %s", e)
            raise e(msg = msg)

        LOG.info("recreateVM :Exit")

        return vm_moref.value


if __name__ == '__main__':
    prop_dict = {
        'memoryMB': 1024,
        'numCPU': 2,
        'numCoresPerSocket': 1,
        'virtualICH7MPresent': False,
        'virtualSMCPresent': False,
        "defaultPowerOps": {
                "defaultResetType": "soft",
                "defaultSuspendType": "hard",
                "suspendType": "hard",
                "standbyAction": "checkpoint",
                "defaultPowerOffType": "soft",
                "resetType": "soft",
                "powerOffType": "soft"
        },
        'bootOptions': {
            'bootDelay': 1,
            'enterBIOSSetup': False,
            'bootRetryEnabled': False,
            'bootRetryDelay': 1,
            'networkBootProtocol': ''
        },
        'tools': '',
        'flags': '',
        #'guestId': '',
        'alternateGuestName': 'testalt',
        'annotation': '',
        #'version': '1.0',
        'memoryHotAddEnabled': False,
        'cpuHotAddEnabled': False,
        'changeVersion': '1.1',
        'cpuAllocation': {
            'reservation': 5,
            'limit': 5,
            'expandableReservation': False,
            'shares': {
                "level": 'normal',
                'shares': 1000
            }
        },
        "cpuHotRemoveEnabled": True,
        "guestAutoLockEnabled": False,
        "maxMksConnections": 5,

        'memoryAllocation': {
            'reservation': 5,
            'limit': 5,
            'expandableReservation': False,
            'shares': {
                "level": 'normal',
                'shares': 1000
            }
        },
        "memoryReservationLockedToMax": False,
        "npivTemporaryDisabled": False,
        "vAssertsEnabled": False,
        "swapPlacement": "yes",
        "firmware": "f1",
        "extraConfig": {
            "key1": "value1"
        },
        'hardware': [
            {
                "VirtualLsiLogicController": {
                    "deviceInfo": {"label": "l1", "summary": "s1"},
                    "busNumber": 2,
                    "sharedBus": "noSharing",
                    "key": 1
                },
                "VirtualLsiLogicSASController": {
                    "deviceInfo": {"label": "l2", "summary": "s2"},
                    "busNumber": 2,
                    "sharedBus": "noSharing",
                    "key": 2
                },
                "ParaVirtualSCSIController": {
                    "deviceInfo": {"label": "l3", "summary": "s3"},
                    "busNumber": 2,
                    "sharedBus": "noSharing",
                    "key": 3
                },
                "VirtualDisk": {
                    "deviceInfo": {"label": "l4", "summary": "s4"},
                    "busNumber": 2,
                    "sharedBus": "noSharing",
                    "key": 4,
                    "backing": {
                        "diskMode": "persistent",
                        "deviceName": "d1",
                        "useAutoDetect": True,
                        "port": {
                            "switchUuid": "1234"
                        }
                    },
                    "capacityInKB": 100000
                },
                "VirtualE100": {
                    "deviceInfo": {"label": "l5", "summary": "s5"},
                    "busNumber": 2,
                    "sharedBus": "noSharing",
                    "key": 1,
                    "backing": {
                        "diskMode": "persistent",
                        "deviceName": "d1",
                        "useAutoDetect": True,
                        "network": {
                            "value": 1,
                            "_type": True
                        },
                        "port": {
                            "switchUuid": "1234"
                        }
                    },
                    "capacityInKB": 100000
                },
                "VirtualVmxnet": {
                    "deviceInfo": {"label": "l6", "summary": "s6"},
                    "busNumber": 2,
                    "sharedBus": "noSharing",
                    "key": 1,
                    "backing": {
                        "diskMode": "persistent",
                        "deviceName": "d1",
                        "useAutoDetect": True,

                        "port": {
                            "switchUuid": "1234"
                        }
                    },
                    "capacityInKB": 100000
                },
                "VirtualPCNet32": {
                    "deviceInfo": {"label": "l7", "summary": "s7"},
                    "busNumber": 2,
                    "sharedBus": "noSharing",
                    "key": 1,
                    "backing": {
                        "diskMode": "persistent",
                        "deviceName": "d1",
                        "useAutoDetect": True,
                        "network": {
                            "value": 1,
                            "_type": True
                        },
                        "port": {
                            "switchUuid": "1234"
                        }
                    },
                    "capacityInKB": 100000
                },
                "VirtualAHCIController": {
                    "deviceInfo": {"label": "l9", "summary": "s9"},
                    "busNumber": 2,
                    "sharedBus": "noSharing",
                    "key": 1,
                    "backing": {
                        "diskMode": "persistent",
                        "deviceName": "d1",
                        "useAutoDetect": True,
                        "network": {
                            "value": 1,
                            "_type": True
                        },
                        "port": {
                            "switchUuid": "1234"
                        }
                    },
                    "capacityInKB": 100000
                },
                "VirtualCdrom": {
                    "deviceInfo": {"label": "l10", "summary": "s10"},
                    "busNumber": 2,
                    "sharedBus": "noSharing",
                    "key": 1,
                    "backing": {
                        "diskMode": "persistent",
                        "deviceName": "d1",
                        "useAutoDetect": True,
                        "port": {
                            "switchUuid": "1234"
                        }
                    },
                    "capacityInKB": 100000,
                    "connectable": {
                        "startConnected": True,
                        "allowGuestControl": True,
                        "connected": True
                    }
                },
                "VirtualFloppy": {
                    "deviceInfo": {"label": "l11", "summary": "s11"},
                    "busNumber": 2,
                    "sharedBus": "noSharing",
                    "key": 1,
                    "backing": {
                        "diskMode": "persistent",
                        "deviceName": "d1",
                        "useAutoDetect": True,
                        "port": {
                            "switchUuid": "1234"
                        }
                    },
                    "capacityInKB": 100000,
                    "connectable": {
                        "startConnected": True,
                        "allowGuestControl": True,
                        "connected": True
                    }
                }

            }
        ]
    }


    #find_datastore('datastore1')
    spec =  buildSpec_for_VM_ConfigInfo(VM_NAME, DATASTORE_NAME, 'ds-123', prop_dict, is_reconfigure=True)
    si = connect_vcenter()
    content = si.RetrieveContent()
    datacenter = content.rootFolder.childEntity[0]
    vmfolder = datacenter.vmFolder
    hosts = datacenter.hostFolder.childEntity
    resource_pool = hosts[0].resourcePool
    task = vmfolder.CreateVM_Task(config=spec, pool=resource_pool)
    wait_for_task(task)