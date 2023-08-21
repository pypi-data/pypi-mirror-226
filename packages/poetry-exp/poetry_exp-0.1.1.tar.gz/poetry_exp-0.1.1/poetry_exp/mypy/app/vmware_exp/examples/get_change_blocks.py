
from pyVim import connect
from pyVmomi import vim

import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
ssl_context.verify_mode = ssl.CERT_NONE

HOST = "172.17.29.xxx"
USER = "administrator@vsphere.local"
PASSWORD = "******"
PORT = 443


def connect_vcenter(host=HOST, username=USER, password=PASSWORD, port=PORT):
    print('connecting to vcenter...')
    service_instance = connect.SmartConnect(host=host,
                                            user=username,
                                            pwd=password,
                                            port=port,
                                            sslContext=ssl_context)
    print ('connected, vcenter: %s', service_instance)
    return service_instance


def wait_for_task(task, return_task=False):
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            print (f'Task done, result: {task.info.result}')
            if return_task:
                return task
            return task.info.result
        if task.info.state == 'error':
            print (f'Task failed: error: {task.info.error.msg}')
            task_done = True
            if return_task:
                return task
            return task.info.error.msg


def lookup_object(vimtype, name):
    """Look up an object by name.

    Args:
      vimtype (object): currently only ``vim.VirtualMachine``
      name (str): Name of the object to look up.
    Returns:
      object: Located object
    """
    si = connect_vcenter()
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vimtype], True)
    for item in container.view:
        if item.name == name:
            return item
    return None


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
        wait_for_task(task)
    else:
        print(f'CBT already enabled')


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


if __name__ == '__main__':
    virtual_machine_name = 'win2016_cbt_test_vm1'
    vm = lookup_object(vim.VirtualMachine, virtual_machine_name)
    print(f'VM: {vm}')
    # enable_cbt(vm)
    change_id = "*"
    get_changed_blocks(vm, change_id=change_id)
