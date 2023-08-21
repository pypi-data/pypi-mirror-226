from pyVmomi import vim
import  logging


def waitForTask(task):
    while True:
        if task.info.state == 'success':
            return task.info.result
        elif task.info.state == 'error':
            return task.info.error.msg

def powerOffVM(vm):
    """
    Description: Power off vm
    Parameters: vmObj: VM object(OBJ)
    Return: None
    """
    # Checking the State of VM power off or on
    if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        # Power off VM
        task = vm.PowerOff()
        # Waiting for power Off
        waitForTask(task)
        logging.info("VM {} power off completed successfully".format(vm.name))


def powerOnVM(vm):
    """
    Description: Power on vm
    Parameters: vm: VM object(OBJ)
    Return: None
    """
    # Checking the State of VM power off or on
    if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOff:
        # Power on VM
        task = vm.PowerOn()
        # Waiting for power on
        waitForTask(task)
        logging.info("Power on VM Completed %s", vm.name)