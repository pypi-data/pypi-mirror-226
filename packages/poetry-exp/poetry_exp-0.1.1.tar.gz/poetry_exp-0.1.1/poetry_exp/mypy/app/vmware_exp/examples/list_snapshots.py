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


def list_snapshots(snapshot):
    snap_names = []
    snap_list = snapshot.rootSnapshotList
    for snap in snap_list:
        snap_name = snap.name
        print(f"Current Snap: {snap_name}")
        snap_names.append(snap_name)
        child_snap_list = snap.childSnapshotList
        while child_snap_list:
            for child_snap in child_snap_list:
                child_snap_name = child_snap.name
                print(f"child_snap_name: {child_snap_name}")
                child_snap_list = child_snap.childSnapshotList


def get_previous_snapshot(snapshot, snap_moref):
    previous_snap_to_given_snap = snap_moref
    snap_names = []
    snap_list = snapshot.rootSnapshotList
    for snap in snap_list:
        snap_name = snap.name
        curr_snap_moref = snap.snapshot._moId
        print(f"Current Snap: {snap_name}, snapshot moref: {curr_snap_moref}")
        if curr_snap_moref == snap_moref:
            print(f'Previous snapshot is: {previous_snap_to_given_snap} for given snapshot: {snap_moref}')
            return previous_snap_to_given_snap
        previous_snap_to_given_snap = curr_snap_moref
        snap_names.append(snap_name)
        child_snap_list = snap.childSnapshotList
        while child_snap_list:
            for child_snap in child_snap_list:
                child_snap_name = child_snap.name
                child_snap_moref = child_snap.snapshot._moId
                print(f"child_snap_name: {child_snap_name}, child_snap_moref: {child_snap_moref}")
                child_snap_list = child_snap.childSnapshotList
                if child_snap_moref == snap_moref:
                    print(f'Previous snapshot is: {previous_snap_to_given_snap} for given snapshot: {snap_moref}')
                    return previous_snap_to_given_snap
                previous_snap_to_given_snap = child_snap_moref
    raise Exception(f"Provided snapshot:{snap_moref} not found in snapshot chain")


def get_snapshot_by_moref(snap_moref):
    snap_properties =\
        vcenter_utils.get_object_by_moref('VirtualMachineSnapshot', snap_moref, ["config"])
    print(snap_properties)

if __name__ == '__main__':

    virtual_machine_name = 'primira_small_vm4'

    vm = vcenter_utils.lookup_object(vim.VirtualMachine, virtual_machine_name)
    print(f'VM: {vm.__dict__}')
    list_snapshots(vm.snapshot)
    # get_previous_snapshot(vm.snapshot, 'snapshot-31039')

    #get_snapshot_by_moref('snapshot-31038')
    # snapshot = take_snapshot(vm)
    # print(snapshot)
    # print(snapshot.__dict__)
    # print(snapshot.config)
