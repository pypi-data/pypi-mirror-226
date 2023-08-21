import re
import time
from pyVmomi import vim, vmodl
from vmware_exp.examples import vcenter_utils


def get_vm_virtual_disk_device_config_spec(
        backing_file_name, backing_device_name, controller_key, unit_number,
        virtual_device_key, operation, file_operation=None,
        backing_type="VirtualDiskFlatVer2BackingInfo",
        is_thin_provisioned=False, disk_mode='independent_persistent',
        disk_compatibility_mode='physicalMode', sharing_mode='sharingNone'):

    vm_virtual_disk_spec = None
    if operation == 'add':
        if backing_type in "VirtualDiskFlatVer1BackingInfo":
            backing = vim.VirtualDiskFlatVer1BackingInfo(
                fileName=backing_file_name, diskMode=disk_mode)

        elif backing_type in "VirtualDiskFlatVer2BackingInfo":
            backing = vim.VirtualDiskFlatVer2BackingInfo(
                fileName=backing_file_name, diskMode=disk_mode,
                thinProvisioned=is_thin_provisioned, sharing=sharing_mode)

        elif backing_type in "VirtualDiskRawDiskMappingVer1BackingInfo":
            backing = vim.VirtualDiskRawDiskMappingVer1BackingInfo(
                fileName=backing_file_name, deviceName=backing_device_name,
                diskMode=disk_mode, compatibilityMode=disk_compatibility_mode,
                sharing=sharing_mode)

        elif backing_type in "VirtualDiskSeSparseBackingInfo":
            backing = vim.VirtualDiskSeSparseBackingInfo(
                fileName=backing_file_name, diskMode=disk_mode)

        elif backing_type in "VirtualDiskSparseVer1BackingInfo":
            backing = vim.VirtualDiskSparseVer1BackingInfo(
                fileName=backing_file_name, diskMode=disk_mode)

        elif backing_type in "VirtualDiskSparseVer2BackingInfo":
            backing = vim.VirtualDiskSparseVer2BackingInfo(
                fileName=backing_file_name, diskMode=disk_mode)
        #
        # vm_virtual_disk_spec = vim.VirtualDeviceConfigSpec(
        #     operation=operation, fileOperation=file_operation,
        #     device=vim.VirtualDisk(backing=backing, key=virtual_device_key,
        #                            unitNumber=unit_number,
        #                            controllerKey=controller_key, capacityInKB=1048576))
        vm_virtual_disk_spec = vim.VirtualDeviceConfigSpec(
            operation=operation, fileOperation=file_operation,
            device=vim.VirtualDisk(backing=backing, key=virtual_device_key,
                                   unitNumber=unit_number,
                                   controllerKey=controller_key))
    elif operation == 'remove':
        if backing_type in "VirtualDiskFlatVer1BackingInfo":
            backing = vim.VirtualDiskFlatVer1BackingInfo(
                fileName=backing_file_name, diskMode=disk_mode)

        elif backing_type in "VirtualDiskFlatVer2BackingInfo":
            backing = vim.VirtualDiskFlatVer2BackingInfo(
                fileName=backing_file_name, diskMode=disk_mode)

        elif backing_type in "VirtualDiskRawDiskMappingVer1BackingInfo":
            backing = vim.VirtualDiskRawDiskMappingVer1BackingInfo(
                fileName=backing_file_name, deviceName=backing_device_name,
                diskMode=disk_mode, compatibilityMode=disk_compatibility_mode,
                sharing=sharing_mode)

        elif backing_type in "VirtualDiskSeSparseBackingInfo":
            backing = vim.VirtualDiskSeSparseBackingInfo(
                fileName=backing_file_name)

        elif backing_type in "VirtualDiskSparseVer1BackingInfo":
            backing = vim.VirtualDiskSparseVer1BackingInfo(
                fileName=backing_file_name)

        elif backing_type in "VirtualDiskSparseVer2BackingInfo":
            backing = vim.VirtualDiskSparseVer2BackingInfo(
                fileName=backing_file_name)

        vm_virtual_disk_spec = vim.VirtualDeviceConfigSpec(
            operation=operation, fileOperation=file_operation,
            device=vim.VirtualDisk(backing=backing, key=virtual_device_key,
                                   unitNumber=unit_number,
                                   controllerKey=controller_key))

    vm_config_spec = vim.VirtualMachineConfigSpec()
    vm_config_spec.deviceChange = [vm_virtual_disk_spec]

    return vm_config_spec


def add_new_disk_to_vm(vm_name, disk_path):
    vm = vcenter_utils.lookup_object(vim.VirtualMachine, vm_name)
    ds = vcenter_utils.lookup_object(vim.Datastore, 'NIMBLE_VOL_DS3_17_GB')

    for vdevice in vm.config.hardware.device:
        #print(type(vdevice))

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
    unit_num = 0
    ctrl_key = 1000
    disk_mode = 'persistent'
    backing_type = "VirtualDiskFlatVer2BackingInfo"
    device_name = "Hard disk 1"
    device_key = 2000
    sharing_mode = 'sharingNone'
    disk_compatibility_mode = ""
    print(f'device_key: {device_key}, ctrl_key: {ctrl_key},'
          f' unit_num: {unit_num}, disk_mode: {disk_mode},'
          f' sharing_mode: {sharing_mode},'
          f' device_name: {device_name}, backing_type: {backing_type}')

    add_spec = \
        get_vm_virtual_disk_device_config_spec(
            disk_path, device_name, ctrl_key, unit_num,
            device_key, "add", file_operation='create',
            backing_type=backing_type,
            disk_mode=disk_mode,
            disk_compatibility_mode=disk_compatibility_mode,
            sharing_mode=sharing_mode)
    print(add_spec)
    task = vm.ReconfigVM_Task(spec=add_spec)
    vcenter_utils.wait_for_task(task)


if __name__ == '__main__':
    disk_file_path = "[NIMBLE_VOL_DS1_15_GB] abc_vm1/abc_vm1.vmdk"
    add_existing_disk_to_vm("abc_vm1", disk_file_path)
    #file_path_without_ds_name = disk_file_path[disk_file_path.rindex("]") + 2:]
    #print(file_path_without_ds_name)
