import re
import time
from pyVmomi import vim, vmodl
from vmware_exp.examples import vcenter_utils


def is_file_exist_in_vm(vm_uuid, vm_user_name, vm_psw, file_path):
    try:

        si = vcenter_utils.connect_vcenter()
        content = si.RetrieveContent()
      # if instanceUuid is false it will search for VM BIOS UUID instead
        vm = content.searchIndex.FindByUuid(datacenter=None,
                                            uuid=vm_uuid,
                                            vmSearch=True,
                                            instanceUuid=False)
        print(f'..........vm: {vm}')

        if not vm:
            raise SystemExit("Unable to locate the virtual machine.")

        print(f'........vm.runtime.powerStat: {vm.runtime.powerState}')

        if vm.runtime.powerState != vim.VirtualMachinePowerState.poweredOn:
            raise SystemExit("VM is not powered on.")

        tools_status = vm.guest.toolsStatus
        print(f'toolsStatus: {tools_status}')

        if (tools_status == 'toolsNotInstalled' or
                tools_status == 'toolsNotRunning'):
            raise SystemExit(
                "VMwareTools is either not running or not installed. "
                "Rerun the script after verifying that VMwareTools "
                "is running")

        creds = vim.vm.guest.NamePasswordAuthentication(
            username=vm_user_name, password=vm_psw
        )

        fm = content.guestOperationsManager.fileManager
        print(f'............fm: {fm}')
        files = fm.ListFilesInGuest(vm, creds, file_path)
        if files:
            print(f'...File: {file_path} exist')
            return True

    except vim.fault.FileNotFound as error:
        print(f'...File: {file_path} not exist')
        return False


if __name__ == '__main__':
    vm_uuid = "564d3947-ee33-0f45-1634-fe8dddff12b9"
    vm_user_name = "Administrator"
    vm_psw = "12iso*help"
    program_path = "C:\\Windows\\System32\\ipconfig.exe"
    program_args = "/allcompartments /all"

    is_file_exist_in_vm(vm_uuid, vm_user_name, vm_psw, program_path)


"""
connecting to vcenter...
connected, vcenter: %s 'vim.ServiceInstance:ServiceInstance'
Program submitted, PID is 2756
Program running, PID is 2756
Program 2756 completed with success
"""