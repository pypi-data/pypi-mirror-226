import re
import time
from datetime import datetime
from pyVmomi import vim, vmodl
from app.vmware_exp.examples import vcenter_utils


def take_snapshot(
        vm, snap_name='TestSnap-'+str(datetime.now()),
        quiesce=True, memory=False, description=None):
    # memory: Snapshot the virtual machines's memory
    # quiesce: quiesce the guest file system
    print(f'Taking snapshot of VM: {vm.name}')

    task = vm.CreateSnapshot_Task(
        name=snap_name, description=description,
        memory=memory, quiesce=quiesce)
    return vcenter_utils.wait_for_task(task)


def delete_snapshot(snapshot, removeChildren=True, consolidate=True):
    print(f'Deleting snapshot: {snapshot._moId}')
    delete_snapshot_task = snapshot.RemoveSnapshot_Task(
        removeChildren=removeChildren, consolidate=consolidate)
    vcenter_utils.wait_for_task(delete_snapshot_task)


if __name__ == '__main__':

    virtual_machine_name = 'win2008_VM'
    #virtual_machine_name = 'Restored-win2008-VM11'
    virtual_machine_name = 'Restored-win2008-VM20'
    virtual_machine_name = 'win2016_server'

    vm = vcenter_utils.lookup_object(vim.VirtualMachine, virtual_machine_name)
    print(f'VM: {vm.config}')

    snapshot = take_snapshot(vm)
    # print(snapshot)
    # print(snapshot.__dict__)
    # print(snapshot.config)
