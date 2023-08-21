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
DATASTORE_NAME = 'Nimble-VVOL1'
VM_NAME = "VVOL_VM1"

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

si = connect_vcenter()

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



def recursive_asdict(d):
    """Convert dict having pyvmomi object into serializable format used to convert config object."""
    out = {}
    if d is None:
        return d

    for k, v in d.__dict__.items():
        if k in ['dynamicType', 'dynamicProperty']:
            continue
        elif k == 'network':
            out[k] = {
                "_type": "Network",
                "value": v._moId
            }
        elif k == 'datastore':
            out[k] = {
                "_type": "Datastore",
                "value": v._moId
            }
        elif isinstance(v, list):
            out[k] = []
            for item in v:
                if hasattr(item, '__dict__'):
                    out[k].append(recursive_asdict(item))
                else:
                    out[k].append(item)
        elif hasattr(v, '__dict__') and k != 'level' and k != 'sharedBus':
            out[k] = recursive_asdict(v)
        else:
            out[k] = v
    return out


def process_config_object(prop_dict):
    try:
        LOG.info("###############process_config_object : Enter")
        LOG.info('################# prop_dict: {0}'.format(prop_dict))

        # conf_dict = dict(prop_dict.values()[0])
        conf_dict = prop_dict.__dict__
        snap_config_dict = {}
        LOG.info('################# conf_dict: {0}'.format(conf_dict))
        for ckeys in conf_dict.keys():
            if ckeys == 'alternateGuestName' or ckeys == 'annotation' or ckeys == 'changeVersion' \
                    or ckeys == 'cpuHotAddEnabled' or ckeys == 'cpuHotRemoveEnabled' or ckeys == 'guestId' \
                    or ckeys == 'vAssertsEnabled' or ckeys == 'npivTemporaryDisabled' or ckeys == 'version' \
                    or ckeys == 'guestFullName' or ckeys == 'locationId' or ckeys == 'name' or ckeys == 'npivNodeWorldWideName' \
                    or ckeys == 'npivPortWorldWideName' or ckeys == 'npivWorldWideNameType' or ckeys == 'swapPlacement' \
                    or ckeys == 'template' or ckeys == 'uuid':
                snap_config_dict[ckeys] = conf_dict[ckeys]

            elif ckeys == 'bootOptions' or ckeys == 'consolePreferences' or ckeys == 'cpuAffinity' \
                    or ckeys == 'cpuAllocation' or ckeys == 'defaultPowerOps' \
                    or ckeys == 'files' or ckeys == 'flags' or ckeys == 'memoryAffinity' \
                    or ckeys == 'memoryAllocation' or ckeys == 'tools':
                LOG.info('#################inside boot options ckeys: {0}'.format(ckeys))
                LOG.info('#################inside boot options conf_dict[ckeys]: {0}'.format(conf_dict[ckeys]))

                snap_config_dict[ckeys] = recursive_asdict(conf_dict[ckeys])

            elif ckeys == 'extraConfig':
                exConf_list = []
                exConf_dict = {}
                exConf_list_dict = []
                LOG.info('#################inside extraConfig conf_dict[ckeys]: {0}'.format(conf_dict[ckeys]))

                exConf_list = conf_dict[ckeys]

                for ex in range(len(exConf_list)):
                    exConf_dict = recursive_asdict(exConf_list[ex])
                    if ('ctkEnabled' in exConf_dict.get('key')):
                        LOG.info("Skipping config: " + str(exConf_dict))
                        continue
                    exConf_list_dict.append(exConf_dict)
                snap_config_dict[ckeys] = exConf_list_dict

            elif ckeys == 'hardware':
                h_dict = conf_dict[ckeys].__dict__
                for hkey in h_dict.keys():
                    if hkey == 'memoryMB' or hkey == 'numCPU' or hkey == 'numCoresPerSocket' \
                            or hkey == 'virtualICH7MPresent' or hkey == 'virtualSMCPresent':
                        snap_config_dict[hkey] = h_dict[hkey]

        if 'hardware' in conf_dict:
            hw = conf_dict['hardware'].__dict__.get('device')
            snap_config_dict['hardware'] = []
            device_dict = {}
            for dev in range(len(hw)):
                device_dict = {}
                LOG.info('#################inside hardware hw[dev]: {0}'.format(hw[dev]))
                LOG.info('#################inside hardware hw[dev].__class__.__name__: {0}'.format(
                    hw[dev].__class__.__name__))
                device_dict[hw[dev].__class__.__name__] = recursive_asdict(hw[dev])
                snap_config_dict['hardware'].append(device_dict)

        LOG.info('.................snap_config_dict: {0}'.format(snap_config_dict))
        LOG.info("process_config_object : Exit")
        return snap_config_dict

    except Exception as e:
        LOG.exception("Error while processing the config object:%s", e)
        msg = "Error while processing the config object"
        raise e(msg=msg)



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
                    except Exception as e:
                        LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        LOG.exception(e)
                        msg = _("Found error in collecting config properties of LSI Logic Controller")
                        LOG.info(msg)
                        raise msg

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
                    except Exception as e:
                        LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        LOG.exception(e)
                        msg = _("Found error in collecting config properties of LSI Logic SAS Controller")
                        LOG.info(msg)
                        raise msg

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

                    except Exception as e:
                        LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        LOG.exception(e)
                        msg = _("Found error in collecting config properties of Virtual Disk Information")
                        LOG.info(msg)
                        raise msg

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
                        backing = hw[i][hkeys].get('backing', None)
                        get_network_backing_info(backing, virtDeviceNW.device)
                        deviceKey.append(virtDeviceNW.device.key)

                        if is_reconfigure == False:
                            virtDeviceNW.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

                        virtualDeviceConfig_Spec_list.append(virtDeviceNW)
                    except Exception as e:
                        LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        LOG.exception(e)
                        msg = _("Found error in collecting config properties of Network")
                        LOG.info(msg)
                        raise msg

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
                        LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        LOG.exception(e)
                        msg = _("Found error in collecting config properties of VMX Network")
                        LOG.info(msg)
                        raise msg

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
                        LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        LOG.exception(e)
                        msg = _("Found error in collecting config properties of Network PCNET")
                        LOG.info(msg)
                        raise msg

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
                            if 'deviceName' in hw[i][hkeys]['backing'] and backing.get('deviceName'):
                                VirtualCdromRemoteAtapiBackingInfo.deviceName = backing.get('deviceName')
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
                    except Exception as e:
                        LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        LOG.exception(e)
                        msg = _("Found error in collecting config properties of CDROM")
                        LOG.info(msg)
                        raise (msg)

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
                    except Exception as e:
                        LOG.info(_("Hkeys information is %s") % hw[i][hkeys])
                        LOG.exception(e)
                        msg = _("Found error in collecting config properties of Floppy")
                        LOG.info(msg)
                        raise (msg)

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
                for key, val in prop_dict['defaultPowerOps'].items():
                    setattr(power_option, key, val)
                spec.powerOpInfo = power_option
            elif ckeys == 'bootOptions':
                bootOptions = vim.VirtualMachineBootOptions()
                for key, val in prop_dict['bootOptions'].items():
                    setattr(bootOptions, key, val)
                spec.bootOptions = bootOptions
            elif ckeys == 'tools':
                tools = vim.vm.ToolsConfigInfo()
                for key, val in prop_dict['tools'].items():
                    setattr(tools, key, val)
                spec.tools = tools
            elif ckeys == 'flags':
                flags = vim.vm.FlagInfo()
                for key, val in prop_dict['flags'].items():
                    setattr(flags, key, val)
                spec.flags = flags
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
                extra_configs = []
                for config in prop_dict['extraConfig']:
                    option = vim.option.OptionValue()
                    option.key = config['key']
                    option.value = config['value']
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
        VirtualEthernetCardNetworkBackingInfo.useAutoDetect = backing.get('useAutoDetect', None)
        VirtualDeviceConfigSpecNW.backing = VirtualEthernetCardNetworkBackingInfo
    elif ports:
        LOG.info("Creating a dSwitch virtual port object")
        VirtualEthernetCardDistributedVirtualPortBackingInfo = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
        VirtualEthernetCardDistributedVirtualPortBackingInfo.port = vim.dvs.PortConnection()
        VirtualEthernetCardDistributedVirtualPortBackingInfo.port.switchUuid = ports.get('switchUuid', None)
        VirtualDeviceConfigSpecNW.backing = VirtualEthernetCardDistributedVirtualPortBackingInfo
    LOG.info("Get network backing info : Exit")

import json
class MyJSONEncoder(json.JSONEncoder):
    """A custom JSONEncoder class that knows how to encode core custom
    objects.

    Custom objects are encoded as JSON object literals (ie, dicts) with
    one key, '__TypeName__' where 'TypeName' is the actual name of the
    type to which the object belongs.  That single key maps to another
    object literal which is just the __dict__ of the object encoded."""

    def default(self, obj):
        try:
            # Check for basic type
            return super(MyJSONEncoder, self).default(obj)

        except TypeError:
            if type(obj) in (vim.Network.Summary,
                vim.Datastore.Summary,
                vim.ClusterComputeResource.Summary,
                vim.host.Summary,
                vim.host.Summary.HardwareSummary,
                vim.host.Summary.ConfigSummary,
                vim.Network,
                vim.AboutInfo,
                vim.vm.Summary,
                vim.vm.Summary.ConfigSummary,
                vim.vm.Summary.StorageSummary,
                vim.vm.Summary.GuestSummary,
                vim.Datastore,
                vim.vm.RuntimeInfo,
                vim.vm.ConfigSpec,
                vim.vm.ToolsConfigInfo,
                vim.vm.FlagInfo,
                vim.vm.DefaultPowerOpInfo,
                vim.vm.device.VirtualDeviceSpec,
                 vim.vm.device.VirtualDeviceSpec,
                 vim.vm.device.VirtualLsiLogicController,
                 vim.vm.ProfileSpec,
                 vim.vm.device.VirtualCdrom,
                 vim.vm.device.VirtualCdrom.RemoteAtapiBackingInfo,
                 vim.vm.device.VirtualDevice.ConnectInfo,
                 vim.ResourceAllocationInfo,
                 vim.vm.ConfigSpec.CpuIdInfoSpec,
                 vim.option.OptionValue,
                 vim.vm.BootOptions,
                 vim.vm.BootOptions.BootableDevice,
                 vim.vm.FileInfo,
                 vim.Description,
                 vim.SharesInfo,
                vim.vm.DeviceRuntimeInfo):
                return obj.__dict__
            # For anything else
            return "__{}__".format(obj.__class__.__name__)


if __name__ == '__main__':
    prop_dict = {
        "changeVersion": None,
        "cpuHotRemoveEnabled": False,
        "virtualSMCPresent": False,
        "memoryMB": 4096,
        "npivTemporaryDisabled": True,
        "tools": {
            "beforeGuestStandby": True,
            "beforeGuestShutdown": True,
            "toolsUpgradePolicy": "manual",
            "afterResume": True,
            "afterPowerOn": True,
            "syncTimeWithHost": False,
            "toolsVersion": 0
        },
        "guestFullName": "Microsoft Windows Server 2012 (64-bit)",
        "uuid": "421dbd84-03ab-604b-831b-a66dc1abbe97",
        "cpuAllocation": {
            "reservation": 0,
            "limit": -1,
            "shares": {
                "shares": 2000,
                "level": "normal"
            },
            "expandableReservation": False
        },
        "version": "vmx-14",
        "template": False,
        "memoryAllocation": {
            "reservation": 0,
            "limit": -1,
            "shares": {
                "shares": 40960,
                "level": "normal"
            },
            "expandableReservation": False
        },
        "numCoresPerSocket": 2,
        "files": {
            "suspendDirectory": "[Nimble_VVOL] rfc4122.92d6ad83-d271-4369-bac0-20d24fa4f912/",
            "snapshotDirectory": "[Nimble_VVOL] rfc4122.92d6ad83-d271-4369-bac0-20d24fa4f912/",
            "vmPathName": "[Nimble_VVOL] rfc4122.92d6ad83-d271-4369-bac0-20d24fa4f912/VVOL_VM1.vmx",
            "logDirectory": "[Nimble_VVOL] rfc4122.92d6ad83-d271-4369-bac0-20d24fa4f912/"
        },
        "alternateGuestName": None,
        "virtualICH7MPresent": False,
        "name": "VVOL_VM1",
        "numCPU": 2,
        "extraConfig": [
            {
                "key": "nvram",
                "value": "VVOL_VM1.nvram"
            },
            {
                "key": "pciBridge0.present",
                "value": "True"
            },
            {
                "key": "svga.present",
                "value": "True"
            },
            {
                "key": "pciBridge4.present",
                "value": "True"
            },
            {
                "key": "pciBridge4.virtualDev",
                "value": "pcieRootPort"
            },
            {
                "key": "pciBridge4.functions",
                "value": "8"
            },
            {
                "key": "pciBridge5.present",
                "value": "True"
            },
            {
                "key": "pciBridge5.virtualDev",
                "value": "pcieRootPort"
            },
            {
                "key": "pciBridge5.functions",
                "value": "8"
            },
            {
                "key": "pciBridge6.present",
                "value": "True"
            },
            {
                "key": "pciBridge6.virtualDev",
                "value": "pcieRootPort"
            },
            {
                "key": "pciBridge6.functions",
                "value": "8"
            },
            {
                "key": "pciBridge7.present",
                "value": "True"
            },
            {
                "key": "pciBridge7.virtualDev",
                "value": "pcieRootPort"
            },
            {
                "key": "pciBridge7.functions",
                "value": "8"
            },
            {
                "key": "hpet0.present",
                "value": "True"
            },
            {
                "key": "disk.EnableUUID",
                "value": "True"
            },
            {
                "key": "cpuid.coresPerSocket",
                "value": "2"
            },
            {
                "key": "sched.cpu.latencySensitivity",
                "value": "normal"
            },
            {
                "key": "migrate.hostLog",
                "value": "VVOL_VM1-3586c238.hlog"
            },
            {
                "key": "vmware.tools.internalversion",
                "value": "0"
            },
            {
                "key": "vmware.tools.requiredversion",
                "value": "10336"
            }
        ],
        "hardware": [
            {
                "VirtualIDEController": {
                    "busNumber": 0,
                    "device": [
                        3000
                    ],
                    "deviceInfo": {
                        "label": "IDE 0",
                        "summary": "IDE 0"
                    },
                    "key": 200
                }
            },
            {
                "VirtualIDEController": {
                    "busNumber": 1,
                    "deviceInfo": {
                        "label": "IDE 1",
                        "summary": "IDE 1"
                    },
                    "key": 201
                }
            },
            {
                "VirtualPS2Controller": {
                    "busNumber": 0,
                    "device": [
                        600,
                        700
                    ],
                    "deviceInfo": {
                        "label": "PS2 controller 0",
                        "summary": "PS2 controller 0"
                    },
                    "key": 300
                }
            },
            {
                "VirtualPCIController": {
                    "busNumber": 0,
                    "device": [
                        500,
                        12000,
                        1000,
                        4000
                    ],
                    "deviceInfo": {
                        "label": "PCI controller 0",
                        "summary": "PCI controller 0"
                    },
                    "key": 100
                }
            },
            {
                "VirtualSIOController": {
                    "busNumber": 0,
                    "deviceInfo": {
                        "label": "SIO controller 0",
                        "summary": "SIO controller 0"
                    },
                    "key": 400
                }
            },
            {
                "VirtualKeyboard": {
                    "controllerKey": 300,
                    "unitNumber": 0,
                    "deviceInfo": {
                        "label": "Keyboard ",
                        "summary": "Keyboard"
                    },
                    "key": 600
                }
            },
            {
                "VirtualPointingDevice": {
                    "backing": {
                        "useAutoDetect": False,
                        "deviceName": None,
                        "hostPointingDevice": "autodetect"
                    },
                    "controllerKey": 300,
                    "unitNumber": 1,
                    "deviceInfo": {
                        "label": "Pointing device",
                        "summary": "Pointing device; Device"
                    },
                    "key": 700
                }
            },
            {
                "VirtualMachineVideoCard": {
                    "useAutoDetect": False,
                    "numDisplays": 1,
                    "deviceInfo": {
                        "label": "Video card ",
                        "summary": "Video card"
                    },
                    "controllerKey": 100,
                    "graphicsMemorySizeInKB": 262144,
                    "enable3DSupport": False,
                    "unitNumber": 0,
                    "use3dRenderer": "automatic",
                    "key": 500,
                    "videoRamSizeInKB": 8192
                }
            },
            {
                "VirtualMachineVMCIDevice": {
                    "allowUnrestrictedCommunication": False,
                    "filterEnable": True,
                    "deviceInfo": {
                        "label": "VMCI device",
                        "summary": "Device on the virtual machine PCI bus that provides support for the virtual machine communication interface"
                    },
                    "controllerKey": 100,
                    "unitNumber": 17,
                    "key": 12000,
                    "id": -1
                }
            },
            {
                "VirtualLsiLogicSASController": {
                    "busNumber": 0,
                    "sharedBus": "noSharing",
                    "deviceInfo": {
                        "label": "SCSI controller 0",
                        "summary": "LSI Logic SAS"
                    },
                    "scsiCtlrUnitNumber": 7,
                    "controllerKey": 100,
                    "unitNumber": 3,
                    "key": 1000,
                    "device": [
                        2000
                    ],
                    "hotAddRemove": True
                }
            },
            {
                "VirtualCdrom": {
                    "connectable": {
                        "status": "untried",
                        "allowGuestControl": True,
                        "connected": False,
                        "startConnected": False
                    },
                    "backing": {
                        "useAutoDetect": False,
                        "deviceName": None,
                        "exclusive": False
                    },
                    "deviceInfo": {
                        "label": "CD/DVD drive 1",
                        "summary": "Remote device"
                    },
                    "controllerKey": 200,
                    "unitNumber": 0,
                    "key": 3000
                }
            },
            {
                "VirtualDisk": {
                    "backing": {
                        "sharing": "sharingNone",
                        "uuid": "6000C29a-05e6-ba69-5163-e17b73085736",
                        "diskMode": "persistent",
                        "contentId": "a4e08629e1bd2bae3d8f0404fffffffe",
                        "fileName": "[Nimble_VVOL] rfc4122.92d6ad83-d271-4369-bac0-20d24fa4f912/VVOL_VM1.vmdk",
                        "writeThrough": False,
                        "split": False,
                        "thinProvisioned": True,
                        "datastore": {
                            "_type": "Datastore",
                            "value": "datastore-7284"
                        },
                        "backingObjectId": "rfc4122.ecfa1bc2-6ea8-4e09-89cb-5975e7c34a66",
                        "digestEnabled": False
                    },
                    "diskObjectId": "142-2000",
                    "deviceInfo": {
                        "label": "Hard disk 1",
                        "summary": "2,097,152 KB"
                    },
                    "shares": {
                        "shares": 1000,
                        "level": "normal"
                    },
                    "controllerKey": 1000,
                    "unitNumber": 0,
                    "capacityInBytes": 2147483648,
                    "key": 2000,
                    "storageIOAllocation": {
                        "reservation": 0,
                        "limit": -1,
                        "shares": {
                            "shares": 1000,
                            "level": "normal"
                        }
                    },
                    "capacityInKB": 2097152,
                    "nativeUnmanagedLinkedClone": False
                }
            },
            {
                "VirtualE1000e": {
                    "macAddress": "00:50:56:9d:b0:db",
                    "addressType": "assigned",
                    "resourceAllocation": {
                        "reservation": 0,
                        "share": {
                            "shares": 50,
                            "level": "normal"
                        },
                        "limit": -1
                    },
                    "connectable": {
                        "status": "untried",
                        "allowGuestControl": True,
                        "connected": False,
                        "migrateConnect": "unset",
                        "startConnected": True
                    },
                    "backing": {
                        "useAutoDetect": False,
                        "deviceName": "VM Network",
                        "network": {
                            "_type": "Network",
                            "value": "network-11"
                        }
                    },
                    "deviceInfo": {
                        "label": "Network adapter 1",
                        "summary": "VM Network"
                    },
                    "controllerKey": 100,
                    "unitNumber": 7,
                    "key": 4000,
                    "uptCompatibilityEnabled": False,
                    "wakeOnLanEnabled": True
                }
            }
        ],
        "swapPlacement": "inherit",
        "locationId": None,
        "guestId": "windows8Server64Guest",
        "bootOptions": {
            "enterBIOSSetup": False,
            "bootDelay": 0,
            "networkBootProtocol": "ipv4",
            "efiSecureBootEnabled": False,
            "bootRetryDelay": 10000,
            "bootRetryEnabled": False
        },
        "annotation": None,
        "cpuHotAddEnabled": False,
        "vAssertsEnabled": False,
        "defaultPowerOps": {
            "defaultResetType": "soft",
            "defaultSuspendType": "hard",
            "suspendType": "hard",
            "standbyAction": "checkpoint",
            "defaultPowerOffType": "soft",
            "resetType": "soft",
            "powerOffType": "soft"
        },
        "flags": {
            "diskUuidEnabled": True,
            "faultToleranceType": "unset",
            "snapshotDisabled": False,
            "recordReplayEnabled": False,
            "runWithDebugInfo": False,
            "virtualMmuUsage": "automatic",
            "vvtdEnabled": False,
            "enableLogging": True,
            "snapshotLocked": False,
            "htSharing": "any",
            "virtualExecUsage": "hvAuto",
            "disableAcceleration": False,
            "snapshotPowerOffBehavior": "powerOff",
            "monitorType": "release",
            "vbsEnabled": False,
            "useToe": False,
            "cbrcCacheEnabled": False
        }
    }



    #find_datastore('datastore1')
    spec =  buildSpec_for_VM_ConfigInfo(VM_NAME, DATASTORE_NAME, 'datastore-9381', prop_dict, is_reconfigure=False)

    #spec_dict = json.dumps(spec, cls=MyJSONEncoder, indent=4)
    spec_dict = process_config_object(spec)
    print ('......spec_dict...........'+str(spec_dict))
    # si = connect_vcenter()
    # content = si.RetrieveContent()
    # datacenter = content.rootFolder.childEntity[0]
    # vmfolder = datacenter.vmFolder
    # hosts = datacenter.hostFolder.childEntity
    # resource_pool = hosts[0].resourcePool
    # task = vmfolder.CreateVM_Task(config=spec, pool=resource_pool)
    # wait_for_task(task)