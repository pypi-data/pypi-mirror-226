import re
import time
from datetime import datetime
from pyVmomi import vim, vmodl
from app.vmware_exp.examples import vcenter_utils
import re



CBT_ENABLED_DISKS_PATTERN =\
    r'(^scsi[0-3]:([0-9]|1[0-5]).ctkEnabled$)|(^sata[0-3]:' \
    r'([0-9]|1[0-9]|2[0-9]).ctkEnabled$)|(^ide[0-1]:[0-1].ctkEnabled$)'

def is_cbt_enabled(vm_name):
    vm = vcenter_utils.lookup_object(vim.VirtualMachine, vm_name)
    extra_configs = vm.config.extraConfig
    #print(extra_configs)
    cbt_enabled = False
    cbt_enabled_disks = set()
    for extra_config in extra_configs:
        if 'ctkEnabled' in extra_config.key:
            print(extra_config)
            if extra_config.key == 'ctkEnabled' and extra_config.value.lower() == 'true':
                cbt_enabled = True
            matched = re.match(CBT_ENABLED_DISKS_PATTERN, extra_config.key)
            if matched and extra_config.value.lower() == 'true':
                cbt_enabled_disks.add(extra_config.key)
    print(f'cbt_enabled: {cbt_enabled}')
    print(f'cbt_enabled_disks: {cbt_enabled_disks}')


def enable_cbt(vm, force=False):
    # VM settings->Advanced->
    # Edit configuration parameters->Add configuration params
    # ctkEnabled  TRUE
    # scsi0:0.ctkEnabled
    cbt_enabled = vm.config.changeTrackingEnabled
    print(f'CBT enabled: {cbt_enabled}')
    if cbt_enabled is False or force is True:
        print(f'Enabling CBT....')
        vm_spec = vim.VirtualMachineConfigSpec()
        vm_spec.changeTrackingEnabled = True
        task = vm.ReconfigVM_Task(spec=vm_spec)
        vcenter_utils.wait_for_task(task)
    else:
        print(f'CBT already enabled')


def disable_cbt(vm, force=False):
    # VM settings->Advanced->
    # Edit configuration parameters->Add configuration params
    # ctkEnabled  TRUE
    # scsi0:0.ctkEnabled
    cbt_enabled = vm.config.changeTrackingEnabled
    print(f'CBT enabled: {cbt_enabled}')
    if cbt_enabled or force:
        print(f'Disabling CBT....')
        vm_spec = vim.VirtualMachineConfigSpec()
        vm_spec.changeTrackingEnabled = False
        task = vm.ReconfigVM_Task(spec=vm_spec)
        vcenter_utils.wait_for_task(task)
    else:
        print(f'CBT already disabled')


def get_changed_blocks(vm, device_key=2000, change_id="*"):
    # changeId="52 90 37 ee 50 dc cb 6b-b3 12 7c 48 06 19 7f d4/1")
    print(f'Getting change block info for VM: {vm.name},'
          f' device_key: {device_key}, from change_id: {change_id}')
    start_offset = 0
    length = 0
    offset = 0
    file = open("blockinfo", "w")
    while True:
        # In case of optimized  backup pass changeId as *
        # for incremental it will be the changedId from mob
        changes = vm.QueryChangedDiskAreas(
            snapshot=vm.snapshot.currentSnapshot,
            deviceKey=device_key,  # 2000,20001
            startOffset=start_offset,
            changeId=change_id)
        print(f'Changes: {changes}')
        """
        Changes: (vim.VirtualMachine.DiskChangeInfo) {
               dynamicType = <unset>,
               dynamicProperty = (vmodl.DynamicProperty) [],
               startOffset = 0,
               length = 1073741824,
               changedArea = (vim.VirtualMachine.DiskChangeInfo.DiskChangeExtent) []
        }
        """

        if changes.changedArea:
            for i in range(len(changes.changedArea)):
                length = changes.changedArea[i].length
                offset = changes.changedArea[i].start
                print("offset:" + str(offset) + " Length:" + str(length))
                file.write(str(offset) + "," + str(length) + "\n")

            start_offset = offset + length
            print(f'start_offset: {start_offset}, changes.Length: {changes.length}')

            if start_offset >= changes.length:
                break
        else:
            print(f'No further changes are found for device: {device_key},'
                  f' changes: {changes}')
            break


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


def get_change_id(snapshot_moref_obj, device_key=2000):
    print(snapshot_moref_obj.config)
    print(f'Getting changeId for device_key: {device_key}')
    change_id = None
    for vdevice in snapshot_moref_obj.config.hardware.device:
        if type(vdevice) is vim.vm.device.VirtualDisk:
            backing = vdevice.backing
            virtual_device_key = vdevice.key
            virtual_device_change_id = backing.changeId
            print(f'ChangeId: {virtual_device_change_id},'
                  f' device key: {virtual_device_key}')

            if virtual_device_key == device_key:
                change_id = virtual_device_change_id
    return change_id


def delete_snapshot(snapshot, removeChildren=True, consolidate=True):
    print(f'Deleting snapshot: {snapshot._moId}')
    delete_snapshot_task = snapshot.RemoveSnapshot_Task(
        removeChildren=removeChildren, consolidate=consolidate)
    vcenter_utils.wait_for_task(delete_snapshot_task)


if __name__ == '__main__':
    # snapshot = vcenter_utils.lookup_object(vim.Snapshot, virtual_machine_name)

    #virtual_machine_name = 'win2016_cbt_test_vm1'
    #
    virtual_machine_name = 'win2016_server_test_vm1'

    vm = vcenter_utils.lookup_object(vim.VirtualMachine, virtual_machine_name)
    print(f'VM: {vm}')
    print(is_cbt_enabled(virtual_machine_name))

    # #enable_cbt(vm)
    # enable_cbt(vm, force=True)
    # #
    # #disable_cbt(vm)
    # snapshot = take_snapshot(vm)
    # # # # print(snapshot.__dict__)
    # change_id = get_change_id(snapshot)
    # print(change_id)
    #
    # # time.sleep(10)
    # # delete_snapshot(snapshot)
    # # snapshot = take_snapshot(vm)
    # # change_id = '52 ef 89 84 df 8a 6d 0e-cd ba 02 9f 81 8e 33 f9/41'
    # # change_id = '52 ef 89 84 df 8a 6d 0e-cd ba 02 9f 81 8e 33 f9/60'
    # # # After disabeling enabling CBT
    # change_id = '52 58 4d e5 2c eb ad 23-8a 8d c7 53 2b eb a9 56/4'
    # get_changed_blocks(vm, change_id=change_id)
    # delete_snapshot(snapshot)

    # get_changed_blocks(vm)

    # for i in range(100):
    #     print(f'...........Executing snapshot:{i}')
    #     snapshot = take_snapshot(vm)
    #     # # # print(snapshot.__dict__)
    #     # change_id = get_change_id(snapshot)
    #     # time.sleep(10)
    #     # delete_snapshot(snapshot)
    #     # snapshot = take_snapshot(vm)
    #     # After disabeling enabling CBT
    #     change_id = '52 a8 ae 17 7f 3e 2b 56-f8 92 b5 a3 4e a8 ca 46/4'
    #     get_changed_blocks(vm, change_id=change_id)
    #     delete_snapshot(snapshot)