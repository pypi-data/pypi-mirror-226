from pyVmomi import vim
from pyVim import connect
from pyVmomi import vim
#from conf import constants
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
ssl_context.verify_mode = ssl.CERT_NONE

HOST = '172.17.29.162'#constants.VCENTER_HOST
USER = 'administrator@vsphere.local'#constants.VCENTER_USER
PASSWORD = '12rmc*Help'#constants.VCENTER_PASSWORD
PORT = 443#constants.VCENTER_PORT
DATASTORE_NAME = 'datastore1'
VM_NAME = "test_vm2"

def wait_for_task(task):
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            print ('Task done')
            return task.info.result
        if task.info.state == 'error':
            print ('Task failed')
            task_done = True
            return task.info.error.msg

def connect_vcenter(host=HOST, username=USER, password=PASSWORD, port=PORT):
    print('connecting to vcenter...')
    service_instance = connect.SmartConnect(host=host,
                                            user=username,
                                            pwd=password,
                                            port=port,
                                            sslContext=ssl_context)
    print ('connected, vcenter: %s', service_instance)
    return service_instance


def find_network(network_name):
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.Network], True)
    networks = container.view
    for network in networks:
        print (network.name)
        if network_name == network.name:
            return network


def find_vm(vm_name):
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.VirtualMachine], True)
    vms = container.view
    for vm in vms:
        print (vm.name)
        if vm_name == vm.name:
            return vm

if __name__ == '__main__':
    si = connect_vcenter()
    morefobj = find_vm('testvm2')
    service_content = si.RetrieveContent()
    task_info = service_content.taskManager.CreateTask(obj=morefobj,
                                          taskTypeId = 'VirtualMachineInstantRecoveryTask',
                                          initiatedBy = 'administrator@vsphere.local',
                                          cancelable = False,
                                          parentTaskKey = None)

    task = task_info.task
    task.SetTaskState(state='running', result=None, fault=None)
    import time
    time.sleep(10)
    task.UpdateProgress(percentDone=20)
    local_message = vim.LocalizableMessage(key="NewMessage", message='Cloning VM.......')
    task.SetTaskDescription(description=local_message)

    service_content.eventManager.LogUserEvent(entity=morefobj, msg='aafak Cloning VM')
    task.UpdateProgress(percentDone=100)
    fault_msg = vim.ExtendedFault(faultTypeId='VirtualMachineInstantRecoveryFailedFault')
    fault = vim.LocalizedMethodFault(fault=fault_msg,
                                             localizedMessage='Recovery Failed')
    #task.SetTaskState(state='error', result=None, fault=fault.fault)


    task.SetTaskState(state='success', result="Successuly created VM", fault=None)


