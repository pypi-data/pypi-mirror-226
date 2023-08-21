import re
import time
from pyVmomi import vim, vmodl
from app.vmware_exp.examples import vcenter_utils
import re

CBT_ENABLED_DISKS_PATTERN =\
    r'(^scsi[0-3]:([0-9]|1[0-5]).ctkEnabled$)|(^sata[0-3]:' \
    r'([0-9]|1[0-9]|2[0-9]).ctkEnabled$)|(^ide[0-1]:[0-1].ctkEnabled$)'

def get_vm_extra_config(vm_name):
    vm = vcenter_utils.lookup_object(vim.VirtualMachine, vm_name)
    extra_configs = vm.config.extraConfig
    #print(extra_configs)
    cbt_enabled = False
    cbt_enabled_disks = set()
    for extra_config in extra_configs:
        if 'ctkEnabled' in extra_config.key:
            print(extra_config)
            if extra_config.key == 'ctkEnabled' and\
                    extra_config.value.lower() == 'true':
                cbt_enabled = True
            else:
                matched = re.match(CBT_ENABLED_DISKS_PATTERN, extra_config.key)
                if matched and extra_config.value.lower() == 'true':
                    cbt_enabled_disks.add(extra_config.key)
    print(f'cbt_enabled: {cbt_enabled}')
    print(f'cbt_enabled_disks: {cbt_enabled_disks}')

    for vdevice in vm.config.hardware.device:

        if type(vdevice) is vim.vm.device.VirtualDisk:
            #print(vdevice)
            device_key = vdevice.key
            ctrl_key = vdevice.controllerKey
            unit_num = vdevice.unitNumber
            backing = vdevice.backing
            if type(backing) is vim.vm.device.VirtualDisk.FlatVer2BackingInfo:
                backing_type = "VirtualDiskFlatVer2BackingInfo"
            disk_mode = backing.diskMode
            file_name = backing.fileName

            uuid = backing.uuid
            sharing_mode = backing.sharing
            device_info = vdevice.deviceInfo
            device_name = device_info.label



    print(f'VM: {vm}')


if __name__ == '__main__':
    vm_name = "primera_small_vvol_vm1"
    get_vm_extra_config(vm_name)
