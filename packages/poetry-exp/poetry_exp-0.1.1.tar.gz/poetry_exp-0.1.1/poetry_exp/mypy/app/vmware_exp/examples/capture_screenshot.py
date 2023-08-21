import re
import time
from pyVmomi import vim, vmodl
from app.vmware_exp.examples import vcenter_utils


def capture_screenshot(vm_uuid, vm_user_name, vm_psw, program_path, program_args):
    try:

        si = vcenter_utils.connect_vcenter()
        content = si.RetrieveContent()
        vm = content.searchIndex.FindByUuid(datacenter=None,
                                            uuid=vm_uuid,
                                            vmSearch=True,
                                            instanceUuid=False)
        print(f'..........vm: {vm}')
        if not vm:
            raise SystemExit("Unable to locate the virtual machine.")
        print(f'........vm.runtime.powerStat: {vm.runtime.powerState}')

        try:
            screenshot_task = vm.CreateScreenshot_Task()
            print(f'............screenshot_task: {screenshot_task}')
            file_path = vcenter_utils.wait_for_task(screenshot_task)
            print(f'.........file_path: {file_path}')
            # Task done, result: [1_Production] WIN_TEST_VM/WIN_TEST_VM-4.png

            if file_path and "]" in file_path:
                file_path_wo_ds_name = file_path[file_path.rfind("]")+2:]
            print(f'.........file_path_wo_ds_name: {file_path_wo_ds_name}')

        except IOError as e:
            print(e)

    except vmodl.MethodFault as error:
        print(error)

        print("Caught vmodl fault : " + error.msg)
        return -1
    return 0


if __name__ == '__main__':
    # "42126d07-3528-4c29-7779-1c29983422f6"
    vm_uuid = "564d3947-ee33-0f45-1634-fe8dddff12b9"
    vm_user_name = "Administrator"
    vm_psw = "12iso*help"
    program_path = "C:\\Windows\\System32\\ipconfig.exe"
    program_args = "/allcompartments /all"

    capture_screenshot(vm_uuid, vm_user_name, vm_psw, program_path, program_args)


"""
connecting to vcenter...
connected, vcenter: %s 'vim.ServiceInstance:ServiceInstance'
Program submitted, PID is 2756
Program running, PID is 2756
Program 2756 completed with success
"""