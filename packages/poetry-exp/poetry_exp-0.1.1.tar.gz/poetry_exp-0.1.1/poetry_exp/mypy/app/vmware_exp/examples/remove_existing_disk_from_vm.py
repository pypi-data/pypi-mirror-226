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


def remove_existing_disk_from_vm(vm_name, disk_path):
    vm = vcenter_utils.lookup_object(vim.VirtualMachine, vm_name)
    print(f'VM: {vm}')
    found_device = False

    for vdevice in vm.config.hardware.device:

        if type(vdevice) is vim.vm.device.VirtualDisk:

            backing = vdevice.backing
            file_name = backing.fileName

            if file_name == disk_file_path:
                found_device = True
                print(f'Found disk: ')
                device_key = vdevice.key
                ctrl_key = vdevice.controllerKey
                unit_num = vdevice.unitNumber

                disk_mode = backing.diskMode
                sharing_mode = backing.sharing
                device_info = vdevice.deviceInfo
                device_name = device_info.label

                if type(backing) is vim.vm.device.VirtualDisk.FlatVer2BackingInfo:
                    backing_type = "VirtualDiskFlatVer2BackingInfo"

                print(f'device_key: {device_key}, ctrl_key: {ctrl_key},'
                      f' unit_num: {unit_num}, disk_mode: {disk_mode},'
                      f' sharing_mode: {sharing_mode},'
                      f' device_name: {device_name}, backing_type: {backing_type}')

                break

    print(f'found_device: {disk_file_path}: {found_device}')

    # del_spec = get_vm_virtual_disk_device_config_spec(
    #     disk_path, None, ctrl_key, unit_num,
    #     device_key, "remove", file_operation="destroy",
    #     backing_type=backing_type)

    # only detach not destroy
    del_spec = get_vm_virtual_disk_device_config_spec(
        disk_path, None, ctrl_key, unit_num,
        device_key, "remove", file_operation=None,
        backing_type=backing_type)
    task = vm.ReconfigVM_Task(spec=del_spec)
    vcenter_utils.wait_for_task(task)


if __name__ == '__main__':
    disk_file_path = "[NIMBLE_VOL_DS1_15_GB] abc_vm1/abc_vm1.vmdk"
    remove_existing_disk_from_vm("abc_vm1", disk_file_path)
