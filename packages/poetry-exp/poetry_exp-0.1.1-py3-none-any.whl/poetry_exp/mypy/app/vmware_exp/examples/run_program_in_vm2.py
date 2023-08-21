import re
import time
from pyVmomi import vim, vmodl
from vmware_exp.examples import vcenter_utils


def run_program_in_vm(vm_uuid, vm_user_name, vm_psw, program_path, program_args):
    try:

        si = vcenter_utils.connect_vcenter()
        content = si.RetrieveContent()
      # if instanceUuid is false it will search for VM BIOS UUID instead
        vm = content.searchIndex.FindByUuid(datacenter=None,
                                            uuid=vm_uuid,
                                            vmSearch=True,
                                            instanceUuid=False)
        print(f'..........vm: {vm}')
        print(f'..........vm: {type(vm)}')

        if not vm:
            raise SystemExit("Unable to locate the virtual machine.")

        print(f'........vm.runtime.powerStat: {vm.runtime.powerState}')

        if vm.runtime.powerState != vim.VirtualMachinePowerState.poweredOn:
            raise SystemExit("VM is not powered on.")

        print(f'........vm: {dir(vm)}')
        tools_status = vm.guest.toolsStatus
        print(f'........toolsStatus: {tools_status}')

        if (tools_status == 'toolsNotInstalled' or
                tools_status == 'toolsNotRunning'):
            raise SystemExit(
                "VMwareTools is either not running or not installed. "
                "Rerun the script after verifying that VMwareTools "
                "is running")

        creds = vim.vm.guest.NamePasswordAuthentication(
            username=vm_user_name, password=vm_psw
        )

        try:
            pm = content.guestOperationsManager.processManager

            ps = vim.vm.guest.ProcessManager.ProgramSpec(
                programPath=program_path,
                arguments=program_args
            )
            res = pm.StartProgramInGuest(vm, creds, ps)
            print(f'........res: {res}')

            if res > 0:
                print("Program submitted, PID is %d" % res)
                pid_exitcode = pm.ListProcessesInGuest(vm, creds,
                                                       [res]).pop().exitCode
                # If its not a numeric result code, it says None on submit
                while re.match('[^0-9]+', str(pid_exitcode)):
                    print("Program running, PID is %d" % res)
                    time.sleep(5)
                    pid_exitcode = pm.ListProcessesInGuest(vm, creds,
                                                           [res]).pop().\
                        exitCode
                    if pid_exitcode == 0:
                        print ("Program %d completed with success" % res)
                        break
                    # Look for non-zero code to fail
                    elif re.match('[1-9]+', str(pid_exitcode)):
                        print ("ERROR: Program %d completed with Failute" % res)
                        # print("  tip: Try running this on guest %r to debug" \
                        #     % summary.guest.ipAddress)
                        print("ERROR: More info on process")
                        print(pm.ListProcessesInGuest(vm, creds, [res]))
                        break

        except IOError as e:
            print(e)

    except vmodl.MethodFault as error:
        print(error)

        print("Caught vmodl fault : " + error.msg)
        return -1
    return 0


if __name__ == '__main__':
    vm_uuid = "564d3947-ee33-0f45-1634-fe8dddff12b9"
    vm_user_name = "Administrator"
    vm_psw = "12iso*help"
    program_path = "C:\\Windows\\System32\\ipconfig.exe"
    program_args = "/allcompartments /all"

    run_program_in_vm(vm_uuid, vm_user_name, vm_psw, program_path, program_args)


"""
connecting to vcenter...
connected, vcenter: %s 'vim.ServiceInstance:ServiceInstance'
Program submitted, PID is 2756
Program running, PID is 2756
Program 2756 completed with success
"""