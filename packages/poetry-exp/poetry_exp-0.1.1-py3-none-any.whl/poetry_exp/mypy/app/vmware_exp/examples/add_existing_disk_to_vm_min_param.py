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


def add_existing_disk_to_vm(vm_name, disk_path, disk_mode, sharing_mode, is_thin_provisioned=None):
    vm = vcenter_utils.lookup_object(vim.VirtualMachine, vm_name)
    print(f'VM: {vm}')
    cont_key_unit_no_map = dict()
    for vdevice in vm.config.hardware.device:
        # if isinstance(vdevice, vim.vm.device.VirtualSCSIController):
        #     cont_key_unit_no_map[vdevice.controllerKey] = {"unitNumber": 0, "deviceKey": 2000}
        #     print(f'Inside VirtualSCSIController: cont_key_unit_no_map: {cont_key_unit_no_map}')

        if type(vdevice) is vim.vm.device.VirtualDisk:
            device_key = vdevice.key
            ctrl_key = vdevice.controllerKey
            unit_num = vdevice.unitNumber
            cont_key_unit_no_map[ctrl_key] = {"unitNumber": unit_num, "deviceKey": device_key}
            print(f'Inside: cont_key_unit_no_map: {cont_key_unit_no_map}')
            backing = vdevice.backing
            if type(backing) is vim.vm.device.VirtualDisk.FlatVer2BackingInfo:
                backing_type = "VirtualDiskFlatVer2BackingInfo"
            disk_mode = backing.diskMode
            file_name = backing.fileName
            sharing_mode = backing.sharing
            device_info = vdevice.deviceInfo
            device_name = device_info.label
            print(f'device_key: {device_key}, ctrl_key: {ctrl_key},'
                  f' unit_num: {unit_num}'
                  f' device_name: {device_name}')

    print(f'cont_key_unit_no_map: {cont_key_unit_no_map}')

    next_unit_number = None
    controller_key = None
    for ctrl_key, ctrl_details in cont_key_unit_no_map.items():
        unit_number = ctrl_details['unitNumber']
        unit_number += 1
        if unit_number == 7:
            print(f'Reserved unit_number: {unit_number}, taking next one')
            unit_number += 1
            print(f'Next unit_number: {unit_number}')
        elif unit_number == 16:
            # this controller gets full, find slot in other controller
            print(f'Controller: {ctrl_key} gets full, looking in other controller')
            continue

        next_unit_number = unit_number
        controller_key = ctrl_key
        break

    print(f'next_unit_number: {next_unit_number}, controller_key: {controller_key}')
    if next_unit_number is None or controller_key is None:
        if len(cont_key_unit_no_map) == 4:
            raise Exception("Maximum disks limits in a VM reached")
        else:
            raise Exception("Could not find the controller")

    backing = vim.VirtualDiskFlatVer2BackingInfo(
        fileName=disk_path, diskMode=disk_mode,
        thinProvisioned=is_thin_provisioned, sharing=sharing_mode)

    vm_virtual_disk_spec = vim.VirtualDeviceConfigSpec(
        operation="add", fileOperation=None,
        device=vim.VirtualDisk(backing=backing, unitNumber=next_unit_number,
                               controllerKey=controller_key))

    vm_config_spec = vim.VirtualMachineConfigSpec()
    vm_config_spec.deviceChange = [vm_virtual_disk_spec]
    #print(vm_config_spec)
    task = vm.ReconfigVM_Task(spec=vm_config_spec)
    vcenter_utils.wait_for_task(task)


if __name__ == '__main__':
    disk_mode = 'persistent'
    #backing_type = "VirtualDiskFlatVer2BackingInfo"
    sharing_mode = 'sharingNone'
    disk_file_path = "[NIMBLE-VOL-DS1-15-GB] test_vm4/test_vm4_test_attach.vmdk"
    add_existing_disk_to_vm(
        "test_vm4", disk_file_path, disk_mode, sharing_mode)

    # https://encoretechnologies.github.io/blog/2017/10/vmware-disks/
    # https://code.vmware.com/samples/557/add-disk-to-vm#code