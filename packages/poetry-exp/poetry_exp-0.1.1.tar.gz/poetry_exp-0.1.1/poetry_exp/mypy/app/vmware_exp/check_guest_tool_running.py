from pyVmomi import vim
import logging
import time

def isGuestToolsRunning(vm):
    """
    Description: Verify that guest tools are installed and running.
    Parameters: vm: The virtual machine on which to check. (OBJECT)
    Raises: RuntimeError if the guest tools are not installed or not running.
    """
    if vm.guest.toolsVersionStatus2 not in [
            vim.vm.GuestInfo.ToolsVersionStatus.guestToolsCurrent,
            vim.vm.GuestInfo.ToolsVersionStatus.guestToolsUnmanaged,
            vim.vm.GuestInfo.ToolsVersionStatus.guestToolsSupportedNew,
            vim.vm.GuestInfo.ToolsVersionStatus.guestToolsSupportedOld]:
        message = 'Unsupported guest tools status: {}, on vm: {}'.format(
            vm.guest.toolsVersionStatus2, vm.name)
        raise RuntimeError(message)
    return vm.guest.toolsRunningStatus == vim.vm.GuestInfo.ToolsRunningStatus.guestToolsRunning


def ensureGuestToolsRunning(vm, wait_for_install=False):
    """
    Description: Ensure that guest tools are installed and running.
    Parameters: vm: The virtual machine on which to check. (OBJECT)
    Raises: RuntimeError if the guest tools are not installed or not running.
    """
    tools_status_list =[
            vim.vm.GuestInfo.ToolsVersionStatus.guestToolsCurrent,
            vim.vm.GuestInfo.ToolsVersionStatus.guestToolsUnmanaged,
            vim.vm.GuestInfo.ToolsVersionStatus.guestToolsSupportedNew,
            vim.vm.GuestInfo.ToolsVersionStatus.guestToolsSupportedOld]
    if wait_for_install:
        tools_status_list.append(vim.vm.GuestInfo.ToolsVersionStatus.guestToolsNotInstalled)
    if vm.guest.toolsVersionStatus2 not in tools_status_list:
        message = 'Unsupported guest tools status: {}, on vm: {}'.format(
            vm.guest.toolsVersionStatus2, vm.name)
        raise RuntimeError(message)
    waitWithTimeout(
        lambda:
        vm.guest.toolsRunningStatus == vim.vm.GuestInfo.ToolsRunningStatus.guestToolsRunning,
        'Guest Tools start on vm: {}'.format(vm.name)
    )


DEFAULT_INTERVAL_SECS = 1
DEFAULT_TIMEOUT_SECS = 60


def waitWithTimeout(isConditionTrueFn, desc,
                    interval=DEFAULT_INTERVAL_SECS, timeout=DEFAULT_TIMEOUT_SECS):
    """
    Description: Wait for condition to become true, but not more than timeout seconds.
                 E.g.: Waiting for a VM to boot, waiting for a VM to power off,
                       waiting for guest tools to start running on a VM, etc.
    Parameters: isConditionTrueFn: The function to call to check
                    if the condition has become true. (CALLABLE)
                desc: Description of the condition to wait for. (STRING)
                interval: The number of seconds to sleep between checks. (INT)
                timeout: The maximum number of seconds to wait for. (INT)
    Raises: RuntimeError if the task times out.
    """
    totalWaitTime = 0
    while (not isConditionTrueFn()) and totalWaitTime < timeout:
        logging.debug('waiting for %s for %ds', desc, interval)
        time.sleep(interval)
        totalWaitTime += interval
    if not totalWaitTime < timeout:
        message = 'Timed out waiting for {} to complete' .format(desc)
        logging.critical(message)
        raise RuntimeError(message)


