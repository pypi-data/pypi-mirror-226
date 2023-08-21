from pyVmomi import vim, vmodl
from app.vmware_exp.examples import vcenter_utils


def consolidate(vm):
    print('Consolidating VM....')
    consolidation_needed = vm.runtime.consolidationNeeded
    if consolidation_needed:
        task = vm.ConsolidateVMDisks_Task()
        vcenter_utils.wait_for_task(task)
        print(f'Successfully consolidated the VM')
    else:
        print('No consolidation needed')


if __name__ == '__main__':
    virtual_machine_name = 'local_tvm1'
    vm = vcenter_utils.lookup_object(vim.VirtualMachine, virtual_machine_name)
    print(f'VM: {vm}')
    consolidate(vm)




