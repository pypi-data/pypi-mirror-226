

import codecs
import errno
import logging
import os.path
import re
import ssl
import tempfile
import time
import atexit

import requests
from pyVim import connect
from pyVmomi import vim
import xml.etree.ElementTree as ET

from common.log import logDeco
import conf.constants as constants
from conf.constants import DEFAULT_TIMEOUT_SECS, DEFAULT_INTERVAL_SECS, \
    DEFAULT_TIMEOUT_SECS_HOST_REBOOT, REMOTE_EXECUTION_PARAMS as params
from common.restClient import RESTClient
from conf.vCenterConstants import ROOT_RESOURCE_POOL_NAME, BACKUP_TASK_INTERVAL, BACKUP_TASK_TIMEOUT
from common.exception.EHCExceptionHandler import commonExceptionHandler


@logDeco.logFunction
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
        logging.critical(message)
        raise RuntimeError(message)
    waitWithTimeout(
        lambda:
        vm.guest.toolsRunningStatus == vim.vm.GuestInfo.ToolsRunningStatus.guestToolsRunning,
        'Guest Tools start on vm: {}'.format(vm.name)
    )


@logDeco.logFunction
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
        logging.critical(message)
        raise RuntimeError(message)
    return vm.guest.toolsRunningStatus == vim.vm.GuestInfo.ToolsRunningStatus.guestToolsRunning


@logDeco.logFunction
def _ensureGuestDirectory(serviceInstance, virtualMachine, guestOSCredentials, dirName):
    """
    Description: Ensure guest directory exists, creating it if necessary.
                 This function is private as it is automatically called by uploadFileToVM(),
                 and need not be called from outside.
    Parameters: serviceInstance: The ServiceInstance object. (OBJECT)
                virtualMachine: The VirtualMachine object. (OBJECT)
                guestOSCredentials: The credential object for the guest OS. (OBJECT)
                dirName: The directory to be created on the guest. (STRING)
    """
    fm = serviceInstance.content.guestOperationsManager.fileManager
    try:
        fm.MakeDirectoryInGuest(virtualMachine, guestOSCredentials, dirName,
                                createParentDirectories=True)
    except vim.fault.FileAlreadyExists:
        logging.info('Directory %s already exists in guest.', dirName)
        # do nothing, ignore this error.


@logDeco.logFunction
def ensureLocalDirectory(localDirPath):
    """
    Description: Ensure that local directory exists, create it if required.
    Parameters: localDirPath: The path of the directory to create. (STRING)
    Raises: OSError if the directory does not exist and cannot be created.
    """
    try:
        # Try to create the directory without checking, and
        # ignore the error if the directory already exists.
        os.makedirs(localDirPath)
    except OSError as ex:
        # Ignore this error.
        dirAlreadyExists = (ex.errno == errno.EEXIST and os.path.isdir(localDirPath))
        if not dirAlreadyExists:  # A regular file might exist with the same name
            # For all other errors, propagate the exception.
            logging.exception("Could not create local directory %s for storing outfiles",
                              localDirPath)
            raise


@logDeco.logFunction
def _getFileExt(filename):
    """
    Description: Get extension of filename.
    Parameters: filename: The filename whose extension is needed. (STRING)
    Returns: The extension of filename (with the '.'), or '' if the file does not
             have an extension. (STRING)
    """
    return os.path.splitext(filename)[1]


@logDeco.logFunction
def _createTempFile(serviceInstance, virtualMachine, guestOSCredentials, guestOSType, extension=''):
    """
    Description: Create an empty temporary file on the guest.
    Parameters: serviceInstance: ServiceInstance Object (OBJECT)
                virtualMachine: VM Object(OBJECT)
                guestOSCredentials: Credentials to connect to guest OS. (OBJECT)
                guestOSType: Type of guest OS, either OSType.LINUX or
                             OSType.WINDOWS. (INT)
                extension: Extension which the remote file must have.(STRING)
    Return: Remote file name(STRING)
    """
    fm = serviceInstance.content.guestOperationsManager.fileManager
    remoteFilename = fm.CreateTemporaryFileInGuest(
        vm=virtualMachine, auth=guestOSCredentials,
        prefix=params['execution_vm'][guestOSType]['prefix'],
        suffix=''.join([params['execution_vm'][guestOSType]['suffix'], extension]),
        directoryPath=params['execution_vm'][guestOSType]['tmpdir']
    )
    logging.debug('Created remote temp file: %s', remoteFilename)
    return remoteFilename


@logDeco.logFunction
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


@logDeco.logFunction
def makeGuestOSAuthentication(guestUsername, guestPassword):
    """
    Description: Create credential object for guest OS.
    Parameters: guestUsername: Username for guest OS. (STRING)
                guestPassword: Password for guest OS. (STRING)
    Returns: Credential object.
    """
    logging.info("creating cred object with username: %s" %guestUsername)
    cred = vim.vm.guest.NamePasswordAuthentication(
        username=guestUsername, password=guestPassword)
    return cred


@logDeco.logFunction
def deleteDirectoryFromGuest(serviceInstance, virtualMachine, guestOSCredentials, dirName):
    """
    Description: Delete directory from guest.
    Parameters: serviceInstance: The ServiceInstance object. (OBJECT)
                virtualMachine: The VirtualMachine object. (OBJECT)
                guestOSCredentials: The credential object for the guest OS. (OBJECT)
                dirName: The directory to be created on the guest. (STRING)
    """
    ensureGuestToolsRunning(virtualMachine)
    fm = serviceInstance.content.guestOperationsManager.fileManager
    fm.DeleteDirectoryInGuest(virtualMachine, guestOSCredentials, dirName, recursive=False)


@logDeco.logFunction
def uploadFileToVM(serviceInstance, virtualMachine, guestOSCredentials, localFilename, guestOSType,
                   remoteFilename=None, hostIP=None):
    """
    Description: Upload a file to remote VM
    Parameters: serviceInstance: ServiceInstance Object (OBJECT)
                virtualMachine: VM Object(OBJECT)
                guestOSCredentials: The credential object for the guest OS. (OBJECT)
                localFilename: Path of the filename to upload(STRING)
                remoteFilename: Path of the remote file to upload
                hostIP: IP of the server to send https request
                guestOSType: Type of guest OS, either OSType.LINUX or
                             OSType.WINDOWS. (INT)
    Return: Remote file name(STRING)
            This file name will have the same extension
            as localFilename.
    """

    _loggingVMAccess(guestOSCredentials, virtualMachine)
    ensureGuestToolsRunning(virtualMachine)
    _ensureGuestDirectory(serviceInstance, virtualMachine, guestOSCredentials,
                          params['execution_vm'][guestOSType]['tmpdir'])
    fileAttr = vim.vm.guest.FileManager.FileAttributes()
    fm = serviceInstance.content.guestOperationsManager.fileManager
    if not remoteFilename:
        remoteFilename = _createTempFile(
            serviceInstance, virtualMachine,
            guestOSCredentials, guestOSType, _getFileExt(localFilename))
    url = fm.InitiateFileTransferToGuest(
        vm=virtualMachine, auth=guestOSCredentials, guestFilePath=remoteFilename,
        fileAttributes=fileAttr, fileSize=os.stat(localFilename).st_size,
        overwrite=True)
    if '*' in url:
        url = url.replace('*', hostIP)
        logging.debug('URL with IP substitution: %s' % str(url))
    with open(localFilename, 'r+b') as localFile:
        response = requests.put(url, localFile, verify=False)
    response.raise_for_status()
    logging.debug('request to %s succeeded with code %s',
                  url, response.status_code)
    return remoteFilename


@logDeco.logFunction
def downloadFileFromVM(serviceInstance, virtualMachine, guestOSCredentials, remoteFilename, stream=False):
    """
    Description: Download a file from remote VM
    Parameters: serviceInstance: ServiceInstance Object (OBJECT)
                virtualMachine: VM Object(OBJECT)
                guestOSCredentials: The credential object for the guest OS. (OBJECT)
                remoteFilename: Path of the filename to download(STRING)
                stream: Flag to indicate if the entire file contents need to be
                loaded into memory (BOOLEAN)
    Return: Name of the local temporary file which holds the downloaded
            data. (STRING)
            This name will have the same extension as the
            remoteFilename.
    """

    _loggingVMAccess(guestOSCredentials, virtualMachine)
    ensureGuestToolsRunning(virtualMachine)
    ensureLocalDirectory(params['orch_vm']['tmpdir'])
    fm = serviceInstance.content.guestOperationsManager.fileManager
    fto = fm.InitiateFileTransferFromGuest(virtualMachine, guestOSCredentials, remoteFilename)
    # EHCINSTALL-1237: Setting stream=True avoids loading the entire file contents into memory when the call is made.
    url = fto.url
    if ("://*" in url):
        hostAddress = virtualMachine.runtime.host.name
        url = url.replace("://*", "://{}".format(hostAddress))
    r = requests.get(url, stream=stream, verify=False)
    r.raise_for_status()
    logging.debug('request to %s succeeded with code %s',
                  url, r.status_code)
    with tempfile.NamedTemporaryFile(mode='w+b', delete=False,
                                     prefix=params['orch_vm']['prefix'],
                                     suffix=params['orch_vm']['suffix'] + _getFileExt(remoteFilename),
                                     dir=params['orch_vm']['tmpdir']) as fd:

        for chunk in r.iter_content(chunk_size=512) if stream else r.iter_content():
            fd.write(chunk)
        return fd.name

@logDeco.logFunction
def downloadFileFromVMWithLocalPath(serviceInstance, virtualMachine, guestOSCredentials,
                                    remoteFilename, localFilepath, localFilename, stream=False):
    """
    Description: Download a file from remote VM
    Parameters: serviceInstance: ServiceInstance Object (OBJECT)
                virtualMachine: VM Object(OBJECT)
                guestOSCredentials: The credential object for the guest OS. (OBJECT)
                remoteFilename: Path of the filename to download(STRING)
                localFilepath: Path of the file to store(STRING)
                localFilename: file name(STRING)
                stream: Flag to indicate if the entire file contents need to be
                loaded into memory (BOOLEAN)
    Return: Name of the local temporary file which holds the downloaded
            data. (STRING)
            This name will have the same extension as the
            remoteFilename.
    """

    _loggingVMAccess(guestOSCredentials, virtualMachine)
    ensureGuestToolsRunning(virtualMachine)
    ensureLocalDirectory(localFilepath)
    fm = serviceInstance.content.guestOperationsManager.fileManager
    fto = fm.InitiateFileTransferFromGuest(virtualMachine, guestOSCredentials, remoteFilename)
    r = requests.get(fto.url, stream=stream, verify=False)
    r.raise_for_status()
    logging.debug('request to %s succeeded with code %s',
                  fto.url, r.status_code)
    with open(os.path.join(localFilepath, localFilename), 'w+b') as fd:
        for chunk in r.iter_content(chunk_size=512) if stream else r.iter_content():
            fd.write(chunk)
        return fd.name

@logDeco.logFunction
def deleteFileFromGuest(serviceInstance, virtualMachine, guestOSCredentials, remoteFilename):
    """
    Description: Delete a file from remote VM
    Parameters: serviceInstance: ServiceInstance Object (OBJECT)
                virtualMachine: VM Object(OBJECT)
                guestOSCredentials: The credential object for the guest OS. (OBJECT)
                remoteFilename: Path of the filename to delete(STRING)
                guestOSType: Type of guest OS, either OSType.LINUX or
                             OSType.WINDOWS. (INT)
    """
    _loggingVMAccess(guestOSCredentials, virtualMachine)
    ensureGuestToolsRunning(virtualMachine)
    fm = serviceInstance.content.guestOperationsManager.fileManager
    fm.DeleteFileInGuest(virtualMachine, guestOSCredentials, remoteFilename)


@logDeco.logFunction
def runScript(serviceInstance, virtualMachine, guestOSCredentials, guestOSType, scriptDict, hostIP=None):
    """
    Description: Run program on remote VM.
    Parameters: serviceInstance: ServiceInstance Object (OBJECT)
                virtualMachine: VM Object(OBJECT)
                hostIP:IP of the server to send https request
                guestOSCredentials: The credential object for the guest OS. (OBJECT)
                scriptDict: Info about the program to run (DICT)
                        remoteShellPath: [MANDATORY] Remote path of the shell used to
                                execute the script (STRING)
                        localScriptPath: [MANDATORY] Local path of script(STRING)
                        args: [OPTIONAL] List of arguments (LIST)
                        timeout: [OPTIONAL] The maximum time (in seconds) for which to
                                wait for the program to complete.
                        shouldLogArguments: [OPTIONAL] Whether the arguments
                                should appear in the logs. (Default True)
                        interval: The number of seconds to sleep between checks. (INT)
    Return: Tuple of (exitCode, outfile), where:
            exitCode is the exit status of the remote program execution,
            outfile is the name of a temporary file which
                contains the captured output and error streams of the program.
                It is the callers responsibility to delete this file if required.
    """

    _loggingVMAccess(guestOSCredentials, virtualMachine)
    # required parameters and their default values.
    localScriptPath = scriptDict.get('localScriptPath')
    remoteShellPath = scriptDict['remoteShellPath']
    args = scriptDict.get('args', [])
    interval = scriptDict.get('interval', DEFAULT_INTERVAL_SECS)
    timeout = scriptDict.get('timeout', DEFAULT_TIMEOUT_SECS)
    shouldLogArguments = scriptDict.get('shouldLogArguments', False)

    # pre-conditions in guest
    ensureGuestToolsRunning(virtualMachine)
    remoteScriptPath = None
    arglist = []
    if localScriptPath:
        # create temporary files on guest OS to store the script itself and the output file.
        remoteScriptPath = uploadFileToVM(serviceInstance, virtualMachine,
                                          guestOSCredentials, localScriptPath, guestOSType, hostIP=hostIP)
        # Setup the script and the arguemnts to run on guest.
        arglist = [remoteScriptPath]
    remoteOutFilePath = _createTempFile(serviceInstance, virtualMachine,
                                        guestOSCredentials, guestOSType)


    arglist.extend(args)
    arglist += ['>', remoteOutFilePath, '2>&1']  # this works for both linux and windows
    progSpec = vim.vm.guest.ProcessManager.ProgramSpec(
        programPath=remoteShellPath,
        arguments=' '.join(arglist)
    )
    argumentsToPrint = progSpec.arguments if shouldLogArguments else '[ARGUMENTS NOT LOGGED]'
    logging.debug(
        "Running remote command: %s %s\n"
        "on VM: %s\n"
        "with shell: %s\n"
        "command-line: %s\n",
        progSpec.programPath, argumentsToPrint,
        virtualMachine.name,
        progSpec.programPath,
        argumentsToPrint)

    # start the program in guest
    pm = serviceInstance.content.guestOperationsManager.processManager
    pid = pm.StartProgramInGuest(virtualMachine, guestOSCredentials, progSpec)

    # wait for program to exit.
    def hasRemoteProgramExited():
        logging.debug("vm state before: %s", virtualMachine.guest.guestState)
        remoteProcessInfo = pm.ListProcessesInGuest(virtualMachine, guestOSCredentials, [pid])[0]
        logging.debug("vm state after: %s", virtualMachine.guest.guestState)
        attrToCheck = 'exitCode'
        return hasattr(remoteProcessInfo, attrToCheck) and getattr(
            remoteProcessInfo, attrToCheck) is not None
    waitWithTimeout(hasRemoteProgramExited, 'Remote program execution', interval=interval, timeout=timeout)

    # Retrieve information from the program execution.
    remoteProcessInfo = pm.ListProcessesInGuest(virtualMachine, guestOSCredentials, [pid])[0]
    localOutFilePath = downloadFileFromVM(serviceInstance, virtualMachine, guestOSCredentials, remoteOutFilePath)
    # clean-up the outfile as required.
    localOutFilePath = convertToLocalEncoding(localOutFilePath, remoteShellPath)

    logging.debug(
        'Exit Status: %s\n'
        'Local Output File: %s\n',
        remoteProcessInfo.exitCode,
        localOutFilePath)
    logFileContents(localOutFilePath, logging.debug)

    if remoteScriptPath:
        # clean-up the remote files.
        deleteFileFromGuest(serviceInstance, virtualMachine, guestOSCredentials, remoteScriptPath)
    deleteFileFromGuest(serviceInstance, virtualMachine, guestOSCredentials, remoteOutFilePath)

    return remoteProcessInfo.exitCode, localOutFilePath

@logDeco.logFunction
def runRemoteUtility(serviceInstance, virtualMachine, guestOSCredentials, guestOSType, scriptDict):
    """
    Description: Run Utility of remote machine on remote machine.
    Parameters: serviceInstance: ServiceInstance Object (OBJECT)
                virtualMachine: VM Object(OBJECT)
                guestOSCredentials: The credential object for the guest OS. (OBJECT)
                scriptDict: Info about the program to run (DICT)
                        remoteUtilityPath: [MANDATORY] Remote path of the utility
                                            need to execute (STRING)
                        args: [OPTIONAL] List of arguments (LIST)
                        timeout: [OPTIONAL] The maximum time (in seconds) for which to
                                wait for the program to complete.
                        shouldLogArguments: [OPTIONAL] Whether the arguments
                                should appear in the logs. (Default True)
    Return: Tuple of (exitCode, outfile), where:
            exitCode is the exit status of the remote program execution,
            outfile is the name of a temporary file which
                contains the captured output and error streams of the program.
                It is the callers responsibility to delete this file if required.
    """

    _loggingVMAccess(guestOSCredentials, virtualMachine)
    # required parameters and their default values.
    remoteUtilityPath = scriptDict['remoteUtilityPath']
    args = scriptDict.get('args', [])
    timeout = scriptDict.get('timeout', DEFAULT_TIMEOUT_SECS)
    shouldLogArguments = scriptDict.get('shouldLogArguments', False)

    # pre-conditions in guest
    ensureGuestToolsRunning(virtualMachine)

    remoteOutFilePath = _createTempFile(serviceInstance, virtualMachine,
                                        guestOSCredentials, guestOSType)

    # Setup the script and the arguemnts to run on guest.
    args += ['>', remoteOutFilePath, '2>&1']  # this works for both linux and windows

    progSpec = vim.vm.guest.ProcessManager.ProgramSpec(
        programPath=remoteUtilityPath,
        arguments=' '.join(args)
    )

    argumentsToPrint = progSpec.arguments if shouldLogArguments else '[ARGUMENTS NOT LOGGED]'
    logging.debug(
        "Running remote command: %s %s\n"
        "on VM: %s\n",
        progSpec.programPath, argumentsToPrint,
        virtualMachine.name)

    # start the program in guest
    pm = serviceInstance.content.guestOperationsManager.processManager
    pid = pm.StartProgramInGuest(virtualMachine, guestOSCredentials, progSpec)

    # wait for program to exit.
    def hasRemoteProgramExited():
        logging.debug("vm state before: %s", virtualMachine.guest.guestState)
        remoteProcessInfo = pm.ListProcessesInGuest(virtualMachine, guestOSCredentials, [pid])[0]
        logging.debug("vm state after: %s", virtualMachine.guest.guestState)
        attrToCheck = 'exitCode'
        return hasattr(remoteProcessInfo, attrToCheck) and getattr(
            remoteProcessInfo, attrToCheck) is not None
    waitWithTimeout(hasRemoteProgramExited, 'Remote program execution', timeout=timeout)

    # Retrieve information from the program execution.
    remoteProcessInfo = pm.ListProcessesInGuest(virtualMachine, guestOSCredentials, [pid])[0]
    localOutFilePath = downloadFileFromVM(serviceInstance, virtualMachine, guestOSCredentials, remoteOutFilePath)

    logging.debug(
        'Exit Status: %s\n'
        'Local Output File: %s\n',
        remoteProcessInfo.exitCode,
        localOutFilePath)
    logFileContents(localOutFilePath, logging.debug)

    # clean-up the remote files.
    deleteFileFromGuest(serviceInstance, virtualMachine, guestOSCredentials, remoteOutFilePath)

    return remoteProcessInfo.exitCode, localOutFilePath


def logFileContents(localOutFilePath, loggerFn):
    """
    Description: Log contents of file using loggerFn.
    Parameters: localOutFilePath: File path whose contents should be logged. (STRING)
                loggerFn: The function to use for logging.
                            (logging.debug, logging.info, etc.) (CALLABLE)
    """
    with open(localOutFilePath, 'r') as l:
        loggerFn('Output: %s', l.read())


def convertToLocalEncoding(localOutFilePath, remoteShellPath):
    """
    Description: Convert file local encoding, from encoding of shell given in remoteShellPath.
    Parameters: localOutFilePath: The file to convert. (STRING)
                remoteShellPath: The shell whose output the encoding is in. (STRING)
    Return: The new file path with contents in local encoding.
    """
    powershellPath = constants.REMOTE_SHELL_PATH[constants.OSType.WINDOWS]['shell']
    powershellEncoding = constants.REMOTE_SHELL_PATH[constants.OSType.WINDOWS]['shell_encoding']
    if remoteShellPath.lower().strip() == powershellPath.lower().strip():
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False,
                                         prefix=params['orch_vm']['prefix'],
                                         suffix=params['orch_vm']['suffix'] + _getFileExt(localOutFilePath),
                                         dir=params['orch_vm']['tmpdir']) as fd:
            newLocalOutFilePath = fd.name
        with codecs.open(newLocalOutFilePath, 'w', encoding=params['orch_vm']['encoding']) as outfd:
            with codecs.open(localOutFilePath, 'r', encoding=powershellEncoding) as infd:
                for line in infd:
                    outfd.write(line)
        os.remove(localOutFilePath)
        localOutFilePath = newLocalOutFilePath
    return localOutFilePath


@logDeco.logFunction
def waitForTask(task, interval=DEFAULT_INTERVAL_SECS, timeout=DEFAULT_TIMEOUT_SECS):
    """
    Description: Wait for task to complete, but no more than timeout seconds.
    Parameters: task: The task to wait for. (OBJECT)
                interval: The number of seconds to sleep between checks. (INT)
                timeout: The maximum number of seconds to wait for. (INT)
    Raises: RuntimeError if the task gives an error.
    """
    key=None
    try:
        key = task.info.key
        waitWithTimeout(
            lambda: task.info.state in [
                vim.TaskInfo.State.success, vim.TaskInfo.State.error],
            'vSphere task {}'.format(task.info.descriptionId),
            interval, timeout)
    except IOError as e:
        logging.error("Got exception while waiting task to compelete %s" %e.message)
        raise IOError(str(key))
    if task.info.state != vim.TaskInfo.State.success:
        message = 'Error in vSphere task {taskDesc}: {errorMsg}'.format(
            taskDesc=task.info.descriptionId,
            errorMsg=task.info.error.msg)
        logging.critical(message)
        raise RuntimeError(message)
    logging.info('Success for vSphere task %s', task.info.descriptionId)

@logDeco.logFunction
def syncTask(task, interval=DEFAULT_INTERVAL_SECS, timeout=DEFAULT_TIMEOUT_SECS):
    """
    Description: Wait for task to complete, but no more than timeout seconds.
    Parameters: task: The task to wait for. (OBJECT)
                interval: The number of seconds to sleep between checks. (INT)
                timeout: The maximum number of seconds to wait for. (INT)
    Raises: RuntimeError if the task gives an error.
    """
    waitWithTimeout(
        lambda: task.info.state in [
            vim.TaskInfo.State.success, vim.TaskInfo.State.error],
        'vSphere task {}'.format(task.info.descriptionId),
        interval, timeout)
    if task.info.state != vim.TaskInfo.State.success:
        message = 'Error in vSphere task {taskDesc}: {errorMsg}'.format(
            taskDesc=task.info.descriptionId,
            errorMsg=task.info.error.msg)
        logging.critical(message)
    logging.info('Success for vSphere task %s', task.info.descriptionId)
    return task

@logDeco.logFunction
def connectToVcenter(vCenterHost, username, password, portNum=443):
    """
    Description: Performs vCenter connection.
    Parameters: vCenterHost - vCenter server ip address (STRING)
                username - vCenter server username (STRING)
                password - vCenter server password (STRING)
                portNum - Port number for connection, default is 443 (INT)
    Returns: service instance object
    Raises: Raises an exception if vCenter connection fails
    """
    # Get the context
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    sslcontext.verify_mode = ssl.CERT_NONE

    try:
        # Call to connect to given vCenterIP
        serviceInstance = connect.SmartConnect(host=vCenterHost, user=username,
                                               pwd=password, port=portNum,
                                               sslContext=sslcontext)
        logging.info("Connecting to : %s, with username: %s" %(vCenterHost, username))
        return serviceInstance
    except:
        message = "Failed to Connect to -{0} user-{1}".format(vCenterHost, username)
        logging.exception(message)
        raise


@logDeco.logFunction
def disconnectFromVcenter(serviceInstance):
    """
    Description: Disconnect serviceInstance.
    Parameters: serviceInstance: The serviceInstance to disconnect. (OBJECT)
    """
    connect.Disconnect(serviceInstance)


@logDeco.logFunction
def getVSphereObj(content, vimType, name):
    """
    Description: Get the vsphere object associated with a given text name
    Parameters: content: Data object having properties for the
                    ServiceInstance managed object (OBJECT)
                vimType: Managed object type (OBJECT)
                name: Managed object entity name (STRING)
    Return: Matched Managed object (OBJECT)
    """
    container = content.viewManager.CreateContainerView(content.rootFolder,
                                                        vimType, True)
    for vmObj in container.view:
        if vmObj.name == name:
            return vmObj
    return None


@logDeco.logFunction
def getVMByName(serviceInstance, name):
    """
    Description: Find a virtual machine by it's name
    Parameters: serviceInstance: vCenter connection session (OBJECT)
                name: virtual machine name (STRING)
    Return: virtual machine Object (OBJECT)
    Raises: RuntimeError if the virtual machine cannot be found.
    """
    vm = getVSphereObj(serviceInstance.RetrieveContent(), [vim.VirtualMachine], name)
    if vm is None:
        message = "Cannot find virtual machine with name: {}".format(name)
        logging.critical(message)
        raise RuntimeError(message)
    return vm


@logDeco.logFunction
def getVAppByName(serviceInstance, name):
    """
    Description: Find a virtual App by it's name
    Parameters: serviceInstance: vCenter connection session (OBJECT)
                name: virtual App name (STRING)
    Return: virtual machine Object (OBJECT)
    Raises: RuntimeError if the virtual App cannot be found.
    """
    vApp = getVSphereObj(serviceInstance.RetrieveContent(), [vim.VirtualApp], name)
    if vApp is None:
        message = "Cannot find vAPP with name: {}".format(name)
        logging.critical(message)
        raise RuntimeError(message)
    return vApp


@logDeco.logFunction
def exeRemoteCommand(vCenterConfDict, vmConfDict, scriptDict):
    """
    Description: Execute Remote Command on Guest VM
    Parameters: vCenterDict: vCenter info(DICT)
                            host: vCenter IP(STRING)
                            user: User namefor vCenter(STRING)
                            password: Password for vCenter(STRING)
                vmDict: Guest VM info(DICT)
                            vmname: Guest VM Name(STRING)
                            vmusername: Guest VM name(STRING)
                            vmpassword: Guest VM Password(STRING)
                            ostype: Guest OS type, either OSType.LINUX or OSType.WINDOWS(INT)
                scriptDict: Info about the program to run (DICT)
                            remoteShellPath: [MANDATORY] Remote path of the shell used to
                                execute the script (STRING)
                            localScriptPath: [MANDATORY] Local path of script(STRING)
                            args: [OPTIONAL] List of arguments (LIST)
                            timeout: [OPTIONAL] The maximum time (in seconds) for which to
                                wait for the program to complete.
                            interval: The number of seconds to sleep between checks. (INT)
    Return: Tuple of (exitCode, outfile), where:
                exitCode is the exit status of the remote program execution,
                outfile is the name of a temporary file which
                    contains the captured output and error streams of the program.
                    It is the callers responsibility to delete this file if required.
    """
    si = None
    try:
        si = connectToVcenter(
            vCenterConfDict['host'],
            vCenterConfDict['user'],
            vCenterConfDict['password'])
        vm = getVMByName(si, vmConfDict['vmname'])
        cred = makeGuestOSAuthentication(vmConfDict['vmusername'], vmConfDict['vmpassword'])
        exitCode, outFilePath = runScript(
            si, vm, cred, vmConfDict['ostype'],
            scriptDict)
        return exitCode, outFilePath
    except Exception as ex:
        message = "Exception {}: {}".format(type(ex).__name__, str(ex))
        logging.exception(message)
        raise
    finally:
        if si is not None:
            disconnectFromVcenter(si)


@logDeco.logFunction
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


@logDeco.logFunction
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


@logDeco.logFunction
def createTemplate(vm):
    """
    Description: Create template of VM
    Parameters: vm: VM object(OBJ)
    Return: None
    """
    gracefulShutDownVM(vm)
    vm.MarkAsTemplate()
    logging.info("Creation of template completed Successfully")

@logDeco.logFunction
def createVM(serviceInstance, vmConfDict):
    """
    Description : Main function to create a new empty VM instance
    Parameters  serviceInstance: vCenter connection session (OBJECT)
                vmConfDict: Containing new VM details (DICT)
                vmConfDict['name']: Name of the VM to create(STRING)
                vmConfDict['dataCenter']: Datacenter name(STRING)
                vmConfDict['memoryMB']: RAM Size(INT)(OPTIONAL)
                                        default: 4096
                vmConfDict['numCPUs']: Number of CPUs(INT)(OPTIONAL)
                                        default: 1
                vmConfDict['guestId']: Virtual machine guest os identifier(STRING)
                vmConfDict['version']: Virtual system types(STRING)(OPTIONAL)
                                        default: vmx-11
                vmConfDict['resourcePool']: Resource Pool(STRING)
                vmConfDict['dataStore']: Data store name(STRING)
                vmConfDict['hdds']: List for hard disk sizes(LIST)
                vmConfDict['numCdrom']: CD/DVD ROM count(INT)
                vmConfDict['SCSI']: SCSI controller type(LIST)
                vmConfDict['NIC']: NIC List(LIST)
    Return: None
    """
    content = serviceInstance.RetrieveContent()
    # Creating Data Store Path
    dataStorePath = "[{}] {}".format(vmConfDict['dataStore'], vmConfDict['name'][1:])

    vmxFile = vim.vm.FileInfo(vmPathName=dataStorePath)

    emptyVMSpecDict = {'name': vmConfDict['name'],
                       'memoryMB': vmConfDict.get('memoryMB', constants.MEMORYMB),
                       'numCPUs': vmConfDict.get('numCPUs', constants.NUM_CPUS),
                       'files': vmxFile,
                       'guestId': vmConfDict['guestId'],
                       'version': vmConfDict.get('version', constants.VM_VERSION)}

    vmSpec = vim.vm.ConfigSpec(**emptyVMSpecDict)

    # datacenter and Resource pool are mandatory for create VM
    # getting the dacenter object if None raising exception
    # getting the VM resource pool and host object, host object is optional
    # If cluster is input then get Root resource pool and creating VM in Root resource pool

    datacenter = getVSphereObj(content, [vim.Datacenter], vmConfDict['dataCenter'])
    if not datacenter:
        logging.critical("datacenter is not valid %s", vmConfDict['dataCenter'])
        raise Exception("datacenter is not valid %s", vmConfDict['dataCenter'])
    vmResourcePool = getVSphereObj(content, [vim.ResourcePool], vmConfDict['resourcePool'])

    hostObj = getVSphereObj(content, [vim.HostSystem], vmConfDict['hostname'])

    if vmResourcePool is None:
        clusterObj = getVSphereObj(content, [vim.ClusterComputeResource], vmConfDict['clusterName'])
        if clusterObj is None:
            logging.critical("Not a valid Cluster %s", vmConfDict['clusterName'])
            logging.critical("Provide valid resource pool or cluster")
            raise Exception("Not a valid Cluster %s", vmConfDict['clusterName'])
        vmResourcePool = clusterObj.resourcePool
        if vmResourcePool is None:
            logging.critical("Cluster %s does not have a valid Root resource pool, Provide valid resource pool",
                             vmConfDict['clusterName'])
            raise Exception("Cluster %s does not have a valid Root resource pool, Provide valid resource pool",
                            vmConfDict['clusterName'])

    # Get the folder where VMs are kept for this datacenter
    datacenterVmFolder = datacenter.vmFolder

    # Start task to create new VM
    task = datacenterVmFolder.CreateVM_Task(config=vmSpec, pool=vmResourcePool, host=hostObj)

    # Waiting to complete create VM
    waitForTask(task)

    logging.info("Empty VM Created Successfully : %s", vmConfDict['name'])

@logDeco.logFunction
def addSCSIController(vm, scsiInfoDict):
    """
    Description : Add SCSI device to the VM instance
    Parameters: vm: VM instance object (OBJECT)
                scsiInfoDict: SCSI Controller Info(DICT)
                scsiInfoDict(sharing): Scsi controller sharing or Non Sharing
    Return:     None
    """
    # add scsi controller
    devChanges = []
    spec = vim.vm.ConfigSpec()
    scsiCtr = vim.vm.device.VirtualDeviceSpec()
    scsiCtr.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
    scsiCtr.device = vim.vm.device.VirtualLsiLogicSASController()
    scsiCtr.device.deviceInfo = vim.Description()
    scsiCtr.device.slotInfo = vim.vm.device.VirtualDevice.PciBusSlotInfo()
    scsiCtr.device.sharedBus = scsiInfoDict['sharing']
    devChanges.append(scsiCtr)
    spec.deviceChange = devChanges
    task = vm.ReconfigVM_Task(spec=spec)
    waitForTask(task)
    logging.info("SCSI controller added Successfully to VM %s", vm.name)


@logDeco.logFunction
def addNICToVM(vm, network):
    """
    Description : Add NIC device to the VM instance
    Parameters: vm: VM instance object (OBJECT)
                network: Network to which NIC to be added (OBJECT)
    Return:     None
    """
    spec = vim.vm.ConfigSpec()
    nicChange = []

    nicSpec = vim.vm.device.VirtualDeviceSpec()
    nicSpec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
    # Adapter type Vmxnet3
    nicSpec.device = vim.vm.device.VirtualVmxnet3()
    nicSpec.device.deviceInfo = vim.Description()
    nicSpec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
    nicSpec.device.backing.useAutoDetect = False
    nicSpec.device.backing.network = network
    nicSpec.device.backing.deviceName = network.name

    nicSpec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    nicSpec.device.connectable.startConnected = True
    nicSpec.device.connectable.allowGuestControl = True
    nicSpec.device.connectable.connected = False
    nicSpec.device.wakeOnLanEnabled = True

    nicChange.append(nicSpec)
    spec.deviceChange = nicChange
    task = vm.ReconfigVM_Task(spec=spec)
    waitForTask(task)
    logging.info("NIC added successfully to VM %s", vm.name)


def addNICToDvSwitch(serviceInstanceContent, vmObj, portGroupName):
    """
    Description: Add NIC to dvSwitch
    Parameters: serviceInstanceContent: Service instance content
                vmObj: VM Object
                portGroupName: Port group Name
    Return:     None
    Raise:      Runtime exception if port group not found

    """
    vmConfigSpec = vim.vm.ConfigSpec()
    nic = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
    port = vim.dvs.PortConnection()
    deviceSpec = vim.vm.device.VirtualDeviceSpec()

    portGroup = getVSphereObj(serviceInstanceContent, [vim.dvs.DistributedVirtualPortgroup], portGroupName)

    if portGroup is None:
        logging.critical("Standard Port group %s was not found", portGroupName)
        raise Exception("Standard Port group %s was not found", portGroupName)

    dvswitch = portGroup.config.distributedVirtualSwitch

    port.switchUuid = dvswitch.uuid
    port.portgroupKey = portGroup.key
    nic.port = port

    for device in vmObj.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualEthernetCard):
            deviceSpec.device = device
            deviceSpec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
            deviceSpec.device.backing = nic
            vmConfigSpec.deviceChange.append(deviceSpec)

    task = vmObj.ReconfigVM_Task(vmConfigSpec)
    waitForTask(task)
    logging.info("NIC successfully added to dvSwitch")


@logDeco.logFunction
def addCDROMToVM(vm):
    """
    Description:add CD-ROM to VM instance
    Parameters: vmobj: VM instance object (OBJECT)
    Return:     None
    """
    dev_changes = []
    spec = vim.vm.ConfigSpec()
    disk_spec = vim.vm.device.VirtualDeviceSpec()
    disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
    disk_spec.device = vim.vm.device.VirtualCdrom()
    disk_spec.device.deviceInfo = vim.Description()
    disk_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    disk_spec.device.connectable.allowGuestControl = False
    disk_spec.device.connectable.connected = True
    disk_spec.device.connectable.startConnected = True
    disk_spec.device.backing = vim.vm.device.VirtualCdrom.RemotePassthroughBackingInfo()
    disk_spec.device.backing.exclusive = False
    controller = getFreeIdeController(vm)
    disk_spec.device.controllerKey = controller.key
    dev_changes.append(disk_spec)
    spec.deviceChange = dev_changes
    task = vm.ReconfigVM_Task(spec=spec)
    waitForTask(task)
    logging.info("CD/DVD drive added successfully to VM %s", vm.name)


@logDeco.logFunction
def getFreeIdeController(vmObj):
    """
    Description : find free IDE controller in VM
    Parameters: vm: VM instance object (OBJECT)
    Return:     IDE Controller (OBJECT) / None
    """
    for dev in vmObj.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualIDEController):
            # If there are less than 2 devices attached, we can use it.
            if len(dev.device) < 2:
                return dev


@logDeco.logFunction
def attachISO(vm, fullPathToISO, driveNum=None):
    """
    Description: Attach an iso to the VM
    Parameters : vm  - Object of the VM to which iso is to be attached (OBJECT)
                 fullPathToISO - Describes the iso path
    Return     : Task object (OBJECT)
    """
    for device in vm.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualCdrom):
            if driveNum is not None:
                match = re.search(str(driveNum), device.deviceInfo.label)
                if not match:
                    continue
            cdspec = vim.vm.device.VirtualDeviceSpec()
            cdspec.device = device
            cdspec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
            cdspec.device.backing = vim.vm.device.VirtualCdrom.IsoBackingInfo()
            for datastore in vm.datastore:
                cdspec.device.backing.datastore = datastore
                break
            cdspec.device.backing.fileName = fullPathToISO
            cdspec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
            cdspec.device.connectable.connected = True
            cdspec.device.connectable.startConnected = True
            cdspec.device.connectable.allowGuestControl = True
            vmConf = vim.vm.ConfigSpec()
            vmConf.deviceChange = [cdspec]
            task = vm.ReconfigVM_Task(vmConf)
            waitForTask(task)
            logging.info("ISO Attached Successfully %s", fullPathToISO)

def make_datastore_directory(service_instance,
                             directory_name,
                             datastore_name,
                             createParentDirectories=False):
    datacenter, datastore = _getDatacenterDatastore(service_instance, datastore_name)
    if not datacenter or not datastore:
        raise RuntimeError("Could not find the datastore specified %s", datastore_name)

    service_instance.content.fileManager.MakeDirectory('[{0}]/{1}'.format(datastore_name,directory_name), datacenter,createParentDirectories=True)

def copy_datastore_file(service_instance,
                        datastore_name,
                        source_path,
                        destination_path,
                        force=True):
    datacenter, datastore = _getDatacenterDatastore(service_instance, datastore_name)
    if not datacenter or not datastore:
        raise RuntimeError("Could not find the datastore specified %s", datastore_name)

    source_full_path='[{0}]/{1}'.format(datastore_name,source_path)
    destination_full_path='[{0}]/{1}'.format(datastore_name,destination_path)
    task=service_instance.content.fileManager.CopyFile(source_full_path,
                                                           datacenter,
                                                           destination_full_path,
                                                           datacenter,
                                                           force)
    return syncTask(task)

def search_datastore_path(service_instance,
                        datastore_name,
                        path):
    datacenter, datastore = _getDatacenterDatastore(service_instance, datastore_name)
    if not datacenter or not datastore:
        raise RuntimeError("Could not find the datastore specified %s", datastore_name)

    full_path='[{0}]/{1}'.format(datastore_name,path)

    task = datastore.browser.Search(full_path)
    return syncTask(task)

@logDeco.logFunction
def uploadFileToDatastore(serviceInstance, dataStoreName, vCenterHost,
                          localFilePath, remoteFilePathName, vCenterPort=443):
    """
    Description: Upload the file to datastore
    Parameters : serviceInstance - vCenter ServiceInstance (OBJECT)
                 dataStoreName - The name of the datatstore (STRING)
                 vCenterHost - Credentials of the vCenter (STRING)
                 localFilePath - Path of the local file which is to be uploaded (STRING)
                 remoteFilePathName - Path to datastore (STRING)
    Return     : Absolute remote file path (STRING)
    Raises     : Raises an Runtime exception if datastore is not found or failed to upload the file
               : Raises an Runtime exception if put request failed
    """
    # Get the datacenter and datastore from datastore name
    datacenter, datastore = _getDatacenterDatastore(serviceInstance, dataStoreName)

    if not datacenter or not datastore:
        logging.critical("Could not find the datastore specified %s", dataStoreName)
        raise RuntimeError("Could not find the datastore specified %s", dataStoreName)

    # remote_file = "New Template"
    remoteFile = remoteFilePathName
    resource = "/folder" + remoteFile

    params = {"dsName": datastore.info.name,
              "dcPath": datacenter.name}

    http_url = "https://{0}:{1}{2}".format(vCenterHost, vCenterPort, resource)

    # Get the cookie built from the current session
    client_cookie = serviceInstance._stub.cookie
    # Break apart the cookie into it's component parts - This is more than
    # is needed, but a good example of how to break apart the cookie
    # anyways. The verbosity makes it clear what is happening.
    cookie_name = client_cookie.split("=", 1)[0]
    cookie_value = client_cookie.split("=", 1)[1].split(";", 1)[0]
    cookie_path = client_cookie.split("=", 1)[1].split(";", 1)[1].split(";", 1)[0].lstrip()

    cookie_text = " {0}; ${1}".format(cookie_value, cookie_path)

    # Make a cookie
    cookie = dict()
    cookie[cookie_name] = cookie_text

    # Get the request headers set up
    headers = {'Content-Type': 'application/octet-stream'}

    # Get the file to upload ready, extra protection by using with against
    # leaving open threads

    logging.info("Uploading local file %s  to  datastore = %s with name at %s ",
                 localFilePath, dataStoreName, resource)
    with open(localFilePath, "rb") as f:
        # Creating object for rest client
        restClient = RESTClient()
        # Connect and upload the file
        res = restClient.put(http_url, headers=headers, params=params, data=f, cookies=cookie)

    if res.status_code in (requests.codes.OK,
                           requests.codes.CREATED,
                           requests.codes.ACCEPTED):
        logging.info("File %s uploaded successfully to datastore %s request status code %s",
                        localFilePath, dataStoreName, res.status_code)
    else:
        logging.critical("Failed to upload file %s to datastore %s, request status code %s", localFilePath,
                         dataStoreName, res.status_code)
        raise RuntimeError("Could not upload file to datastore")


@logDeco.logFunction
def removeDeviceFromVM(vm, label):
    """
    Description : Delete a device on VM by label
    Parameters: vm: VM instance object (OBJECT)
                label: label of device (STRING)
    Raise:      Runtime Error if device not present
    Return:     None

    """
    labelFound = False
    for device in vm.config.hardware.device:
        if device.deviceInfo.label == label:
            labelFound = True
            virtual_disk_spec = vim.vm.device.VirtualDeviceSpec()
            virtual_disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
            virtual_disk_spec.device = device

            spec = vim.vm.ConfigSpec()
            spec.deviceChange = [virtual_disk_spec]
            task = vm.ReconfigVM_Task(spec=spec)
            waitForTask(task)
            logging.info("Device %s removed successfully from vm %s", label, vm.name)
    if labelFound is False:
        logging.critical("Device does not present with label %s", label)
        raise RuntimeError("Device does not present with label %s", label)

@logDeco.logFunction
def deleteDatastoreFile(serviceInstance, dataStoreFilePath):
    """
    Description: Deletes the datastore file/directory
    Parameters : serviceInstance: vCenter service instance (OBJECT)
                 dataStoreFilePath: Path to datastore file/directory
    Return:     None
    Raises     : Raises an exception if datastore is not found or failed to delete files
    """
    # Get the datacenter and datastore from datastore name
    datastorename = re.match("\[(.*?)\].*", dataStoreFilePath)
    if datastorename is None:
        raise NameError("Path %s does not contain datastore name", dataStoreFilePath)
    dsname = datastorename.group(1)
    datacenter, datastore = _getDatacenterDatastore(serviceInstance, dsname)
    if not datacenter or not datastore:
        raise RuntimeError("Could not find the datastore specified %s", datastorename)
    task = serviceInstance.content.fileManager.DeleteFile(dataStoreFilePath, datacenter)

    return syncTask(task)

@logDeco.logFunction
def _getDatacenterDatastore(serviceInstance, dsname):
    """
    Description:
    Parameters :serviceInstance: vCenter service instance (OBJECT)
                dsname: Datastorename
    Return:     ds: datastore Name
                dc: datacentername
    """
    for dc in serviceInstance.content.rootFolder.childEntity:
        for ds in dc.datastore:
            if ds.name == dsname:
                return dc, ds


@logDeco.logFunction
def detachISO(vm):
    """
    Description: Remove an iso attached to the VM
    Parameters : vm  - Object of the VM to which iso is to be attached (OBJECT)
    Return     : Task object (OBJECT)
    Raises     : Raises an exception if failed to remove the attached ISO
    """
    for device in vm.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualCdrom):
            logging.info("Detaching ISO from %s", device.deviceInfo.label)
            cdspec = vim.vm.device.VirtualDeviceSpec()
            cdspec.device = device
            cdspec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
            cdspec.device.backing = vim.vm.device.VirtualCdrom.RemotePassthroughBackingInfo()
            vmconf = vim.vm.ConfigSpec()
            vmconf.deviceChange = [cdspec]
            task = vm.ReconfigVM_Task(vmconf)
            waitForTask(task)
            logging.info("ISO Detached Successfully %s", device.deviceInfo.label)


def _loggingVMAccess(guestOSCredentials, virtualMachine):
    """
    Description: Function logs username from credentials
    parameters: guestOSCredentials: Guest OS credentials object (OBJECT)
                virtualMachine: VM instance object (OBJECT)

    """
    userName = guestOSCredentials.username
    vmName = virtualMachine.name
    logging.info("VM details are VM name - %s, username - %s"% (vmName, userName))

@logDeco.logFunction
def gracefulShutDownVM(virtualMachine, interval=DEFAULT_INTERVAL_SECS, timeout=DEFAULT_TIMEOUT_SECS):
    """
    Description: Function gracefully Shutdown VM.
    parameters: virtualMachine: VM instance object (OBJECT)
                interval: The number of seconds to sleep between checks. (INT)
                timeout: The maximum number of seconds to wait for. (INT)

    """
    if virtualMachine.runtime.powerState == vim.VirtualMachine.PowerState.poweredOn:
        logging.info('Shutting down guest VM %s', virtualMachine.name)
        virtualMachine.ShutdownGuest()
        waitWithTimeout(
            lambda: virtualMachine.runtime.powerState ==
                    vim.VirtualMachine.PowerState.poweredOff,
            'Guest VM {} Shutdown and PowerOff.'.format(virtualMachine.name),
            interval, timeout)
        logging.info("VM %s powered off, current state is %s", virtualMachine.name, virtualMachine.runtime.powerState)

@logDeco.logFunction
def gracefulStartVM(virtualMachine, interval=DEFAULT_INTERVAL_SECS, timeout=DEFAULT_TIMEOUT_SECS):
    """
    Description: Function gracefully Start VM with gracefully runs Guest Tools.
    parameters: virtualMachine: VM instance object (OBJECT)
                interval: The number of seconds to sleep between checks. (INT)
                timeout: The maximum number of seconds to wait for. (INT)

    """

    if virtualMachine.runtime.powerState == vim.VirtualMachine.PowerState.poweredOff:
        logging.info("Powering On vm %s", virtualMachine.name)
        waitForTask(virtualMachine.PowerOn(), interval,timeout)
        logging.info("VM %s powered on.", virtualMachine.name)
    waitWithTimeout(lambda: virtualMachine.guest.toolsRunningStatus ==
                            vim.vm.GuestInfo.ToolsRunningStatus.guestToolsRunning, 'Guest tools start',
                    interval, timeout)
    logging.info("Guest tools started for VM %s", virtualMachine.name)


@logDeco.logFunction
def setVMCustomizationSpec(serviceInstance, customizationDetails):
    """
    Description: Function to set and save Guest Customization Specifications for new VM
    Parameters: serviceInstance: vCenter service instance (OBJECT)
                customizationDetails: VM Guest customization details (DICTIONARY)
                    customizationDetails["userFullName"]: User full name (STRING)
                    customizationDetails["userOrgName"]: User's organization (STRING)
                    customizationDetails["computerName"]: Computer Name (STRING)
                    customizationDetails["windowsProductKey"]: A valid serial number(a Windows Product Key)(OPTIONAL)(STRING)
                    customizationDetails["domainAdminPassword"]: The domain admin password (STRING)
                    customizationDetails["joinWorkgroup"]: The workgroup that the virtual machine should join (STRING)
                    customizationDetails["joinDomain"]: The domain that the virtual machine should join (STRING)
                    customizationDetails["domainAdmin"]: This is the domain user account used for authentication (STRING)
                    customizationDetails["vmLicenseAutoMode"]: VM license auto mode ("perServer"/"perSeat") (STRING)
                    customizationDetails["vmLicenseAutoUsers"]: The number of client licenses purchased (INTEGER)
                    customizationDetails["administratorPassword"]: The Administrator(user) password (STRING)
                    customizationDetails["vmTimeZone"]: The time zone for the new virtual machine (INTEGER)
                    customizationDetails["vmAutoLogon"]: Logs on as Administrator automatically (BOOLEAN)
                    customizationDetails["vmAutoLogonCount"]: The number of times the machine should automatically log on as Administrator (INTEGER)
                    customizationDetails["vmIPFixedIPAddress"]: Static IP address for new VM (STRING)
                    customizationDetails["vmIPSubnetMask"]: Subnet mask for this virtual network adapter (STRING)
                    customizationDetails["vmIPGateway"]: List of gateways; For a virtual network adapter with a static IP address (LIST)
                    customizationDetails["vmIPDNSServerList"]: A list of server IP addresses to use for DNS lookup in a Windows guest operating system (LIST)
                    customizationDetails["vmCustomSpecInfoName"]: Unique name of the specification (STRING)
                    customizationDetails["vmCustomSpecInfoDescription"]: Description of the specification (STRING)
                    customizationDetails["vmCustomSpecInfoType"]: Guest operating system for this specification (STRING)

    Return: Object of type "vim.vm.customization.Specification" (OBJECT)
    """
    logDict = {}

    # Set User Data in customization
    userData = vim.vm.customization.UserData()
    userData.fullName = customizationDetails.get("userFullName")
    userData.orgName = customizationDetails.get("userOrgName")
    userData.computerName = vim.vm.customization.FixedName()
    userData.computerName.name = customizationDetails.get('computerName', '')
    userData.productId = customizationDetails.get("windowsProductKey")
    logDict.update({"userFullName":userData.fullName, "userOrgName":userData.orgName})

    # Set Domain admin password configuration
    domainAdminPassword = vim.vm.customization.Password()
    domainAdminPassword.value = customizationDetails.get("domainAdminPassword")
    # If password is plain text then the password is not encrypted
    domainAdminPassword.plainText = constants.IS_PASSWORD_PLAIN_TEXT

    # Set Workgroup/Domain configuration. The VM may belong to a workgroup or domain
    customIdentification = vim.vm.customization.Identification()
    if customizationDetails.get("joinWorkgroup", False):
        customIdentification.joinWorkgroup = customizationDetails.get("joinWorkgroup")
        logDict.update({"joinWorkgroup":customIdentification.joinWorkgroup})
    else:
        customIdentification.joinDomain = customizationDetails.get("joinDomain")
        customIdentification.domainAdmin = customizationDetails.get("domainAdmin")
        customIdentification.domainAdminPassword = domainAdminPassword
        logDict.update({"joinDomainName":customIdentification.joinDomain})

    vmLicense = vim.vm.customization.LicenseFilePrintData()
    vmLicense.autoMode = customizationDetails.get("vmLicenseAutoMode")
    if vmLicense.autoMode == constants.VM_LICENSE_AUTO_MODE_PER_SERVER:
        # AutoUsers is valid only if autoMode = "perServer"
        vmLicense.autoUsers = customizationDetails.get("vmLicenseAutoUsers")
    else:
        vmLicense.autoMode = constants.VM_LICENSE_AUTO_MODE_PER_SEAT
    logDict.update({"vmLicenseAutoMode":vmLicense.autoMode})

    # Set Administrator(User) password configuration
    administratorPassword = vim.vm.customization.Password()
    administratorPassword.value = customizationDetails.get("administratorPassword")
    # If password is plain text then the password is not encrypted
    administratorPassword.plainText = constants.IS_PASSWORD_PLAIN_TEXT

    guiUnattended = vim.vm.customization.GuiUnattended()
    guiUnattended.password = administratorPassword
    guiUnattended.timeZone = customizationDetails.get("vmTimeZone")
    guiUnattended.autoLogon = customizationDetails.get("vmAutoLogon")
    if guiUnattended.autoLogon:
        guiUnattended.autoLogonCount = customizationDetails.get("vmAutoLogonCount")
    else:
        guiUnattended.autoLogonCount = constants.ZERO_AUTO_LOGON_COUNT
    logDict.update({"vmTimeZoneID":guiUnattended.timeZone})

    sysPrep = vim.vm.customization.Sysprep()
    # An object representation of the sysprep GuiUnattended key
    sysPrep.guiUnattended = guiUnattended
    # An object representation of the sysprep UserData key
    sysPrep.userData = userData
    # An object representation of the sysprep Identification key
    sysPrep.identification = customIdentification
    # Required only for Windows 2000 Server and Windows Server 2003
    sysPrep.licenseFilePrintData = vmLicense

    # Optional operations supported by the customization process for Windows
    windowsOptions = vim.vm.customization.WinOptions()
    windowsOptions.changeSID = constants.GENERATE_NEW_SECURITY_ID
    windowsOptions.deleteAccounts = constants.DELETE_WINDOWS_ACCOUNTS

    # Set IP settings for a virtual network adapter
    vmIPSettings = vim.vm.customization.IPSettings()
    vmIPSettings.ip = vim.vm.customization.FixedIp()
    vmIPSettings.ip.ipAddress = customizationDetails.get("vmIPFixedIPAddress")
    vmIPSettings.subnetMask = customizationDetails.get("vmIPSubnetMask")
    vmIPSettings.gateway = customizationDetails.get("vmIPGateway")
    vmIPSettings.dnsServerList = customizationDetails.get("vmIPDNSServerList")
    logDict.update({
        "vmIPFixedIPAddress":vmIPSettings.ip.ipAddress,
        "vmIPSubnetMask":vmIPSettings.subnetMask,
        "vmIPGatewayList":vmIPSettings.gateway,
        "vmIPDNSServerList":vmIPSettings.dnsServerList
    })

    vmAdapterMapping = vim.vm.customization.AdapterMapping()
    # The IP settings for the associated virtual network adapter
    vmAdapterMapping.adapter = vmIPSettings

    # Set the Specification data object type which contains information required to customize a virtual machine
    customizationSpec = vim.vm.customization.Specification()
    # Optional operations (either LinuxOptions or WinOptions)
    customizationSpec.options = windowsOptions
    # Network identity and settings, similar to Microsoft's Sysprep tool
    customizationSpec.identity = sysPrep
    # IP settings that are specific to a particular virtual network adapter
    customizationSpec.nicSettingMap = [vmAdapterMapping]
    # A collection of global IP settings for a virtual network adapter
    customizationSpec.globalIPSettings = vim.vm.customization.GlobalIPSettings()

    # Create an instance of customizationSpecManager
    customizationManager = serviceInstance.content.customizationSpecManager

    # Set the public key(Byte array ) used to encrypt any passwords stored in the specification
    customizationSpec.encryptionKey = customizationManager.encryptionKey

    # Set Specification information and the Specification object.
    customSpec = vim.CustomizationSpecItem()
    customSpec.spec = customizationSpec
    customSpec.info = vim.CustomizationSpecInfo()
    customSpec.info.name = customizationDetails.get("vmCustomSpecInfoName")
    customSpec.info.description = customizationDetails.get("vmCustomSpecInfoDescription")
    customSpec.info.type = customizationDetails.get("vmCustomSpecInfoType")

    # Create and save the guest customization specifications
    try:
        customizationManager.CreateCustomizationSpec(item=customSpec)
        logging.info("Saved the Customization Specification: '%s' ", customSpec.info.name)
        logging.info("Details of the saved Customization Specification are as follows: %s", logDict)
    except vim.fault.AlreadyExists:
        customizationManager.OverwriteCustomizationSpec(item=customSpec)
        logging.info("Overwritten the Customization Specification: '%s' ", customSpec.info.name)
        logging.info("Details of the saved Customization Specification are as follows: %s", logDict)
    return customizationSpec


@logDeco.logFunction
def validateVMCustomizationSpec(serviceInstance, customizationDetails):
    """
    Description: Function to set and save Guest Customization Specifications for new VM
    Parameters: serviceInstance: vCenter service instance (OBJECT)
                customizationDetails: VM Guest customization details (DICTIONARY)
                    customizationDetails["vmCustomSpecInfoName"]: Unique name of the specification (STRING)
                    customizationDetails["userFullName"]: User full name (STRING)
                    customizationDetails["userOrgName"]: User's organization (STRING)
                    customizationDetails["joinWorkgroup"]: The workgroup that the virtual machine should join (STRING)
                    customizationDetails["joinDomain"]: The domain that the virtual machine should join (STRING)
                    customizationDetails["vmLicenseAutoMode"]: VM license auto mode ("perServer"/"perSeat") (STRING)
                    customizationDetails["vmTimeZone"]: The time zone for the new virtual machine (INTEGER)
                    customizationDetails["vmAutoLogon"]: Logs on as Administrator automatically (BOOLEAN)
                    customizationDetails["vmAutoLogonCount"]: The number of times the machine should automatically log on as Administrator (INTEGER)
                    customizationDetails["vmIPFixedIPAddress"]: Static IP address for new VM (STRING)
                    customizationDetails["vmIPSubnetMask"]: Subnet mask for this virtual network adapter (STRING)
                    customizationDetails["vmIPGateway"]: List of gateways; For a virtual network adapter with a static IP address (LIST)
                    customizationDetails["vmIPDNSServerList"]: A list of server IP addresses to use for DNS lookup in a Windows guest operating system (LIST)
    Return: validationStatus: Validation status (BOOLEAN)
    """
    # Create an instance of customizationSpecManager
    customSpecManager = serviceInstance.content.customizationSpecManager
    validationStatus = True
    if customSpecManager.DoesCustomizationSpecExist(customizationDetails.get("vmCustomSpecInfoName")):
        customSpec= customSpecManager.GetCustomizationSpec(customizationDetails.get("vmCustomSpecInfoName"))
        customizationSpecification = customSpec.spec
        customSpecDetails = {}
        customSpecDetails["userFullName"] =  customizationSpecification.identity.userData.fullName
        customSpecDetails["userOrgName"] = customizationSpecification.identity.userData.orgName
        if customizationDetails.get("joinWorkgroup"):
            customSpecDetails["joinWorkgroup"] = customizationSpecification.identity.identification.joinWorkgroup
        else:
            customSpecDetails["joinDomain"] = customizationSpecification.identity.identification.joinDomain
        customSpecDetails["vmLicenseAutoMode"] = customizationSpecification.identity.licenseFilePrintData.autoMode
        customSpecDetails["vmTimeZone"] = customizationSpecification.identity.guiUnattended.timeZone
        customSpecDetails["vmAutoLogon"] = customizationSpecification.identity.guiUnattended.autoLogon
        customSpecDetails["vmAutoLogonCount"] = customizationSpecification.identity.guiUnattended.autoLogonCount
        customSpecDetails["vmIPFixedIPAddress"] = customizationSpecification.nicSettingMap[0].adapter.ip.ipAddress
        customSpecDetails["vmIPSubnetMask"] = customizationSpecification.nicSettingMap[0].adapter.subnetMask
        customSpecDetails["vmIPGateway"] = customizationSpecification.nicSettingMap[0].adapter.gateway
        customSpecDetails["vmIPDNSServerList"] = customizationSpecification.nicSettingMap[0].adapter.dnsServerList
        customSpecDetails["vmCustomSpecInfoName"] = customSpec.info.name
        # Validate the Customization Specifications Details
        for key in customSpecDetails.keys():
            if customSpecDetails.get(key) != customizationDetails.get(key):
                validationStatus = False
                logging.info("Unable to validate key:'%s'; actual value: '%s'; expected value: '%s'",
                             key, customSpecDetails.get(key), customizationDetails.get(key))

        # Check the Validation Status
        if validationStatus == True:
            logging.info("Successful validation for creation of Customization Specification: '%s' ", customizationDetails.get("vmCustomSpecInfoName"))
        else:
            logging.info("Validation failed for Customization Specification: '%s' ", customizationDetails.get("vmCustomSpecInfoName"))
    else:
        validationStatus = False
        logging.info("Validation failed for Customization Specification: '%s' ", customizationDetails.get("vmCustomSpecInfoName"))

    return validationStatus


@logDeco.logFunction
def deployVMFromTemplate(serviceInstance, templateName, vmDetails, customSpecVM, interval=DEFAULT_INTERVAL_SECS,
                         timeout=DEFAULT_TIMEOUT_SECS):
    """
    Description: Function to deploy VM from Template
    Parameters: serviceInstance: vCenter service instance (OBJECT)
                templateName: Name of the template to be used to deploy VM (STRING)
                vmDetails: Details of VM [Dictionary]
                    vmDetails['vmName']: Name of the VM to create(STRING)
                    vmDetails['dataCenterName']: Datacenter Name(STRING)
                    vmDetails['vmFolder']:Name of vmFolder, Default - 'dataCenter.vmFolder'(STRING)(OPTIONAL)
                    vmDetails['dataStoreName']:Name of Datastore (STRING)
                    vmDetails['clusterName']: Name of cluster (STRING)
                    vmDetails['resourcePool']: Name of Resource pool (STRING)
                    vmDetails['powerON']:Make VM power on/off (BOOL)
                    vmDetails['vmName'] - name of vm (STRING)
                    vmDetails['cpuConfig'] - cpu configuration
                    vmDetail['vmMemoryConfig'] - memory configuration
                    vmDetail['hddConfig'] - hard disk drive configuration
                customSpecVM: Customization spec dictionary
                interval: The number of seconds to sleep between checks. (INT)
                timeout: The maximum number of seconds to wait for. (INT)
    Return: None
    """

    content = serviceInstance.RetrieveContent()

    template = getVSphereObj(content, [vim.VirtualMachine], templateName)

    # if none get the first one
    dataCenter = getVSphereObj(content, [vim.Datacenter], vmDetails['dataCenterName'])
    try:
        if vmDetails.get('vmFolder'):
            destFolder = getVSphereObj(content, [vim.Folder], vmDetails['vmFolder'])
        else:
            destFolder = dataCenter.vmFolder
        if not destFolder:
            raise
    except:
        message = "Cannot get the VM Folder: %s"%vmDetails.get('vmFolder')
        logging.exception(message)
        raise Exception(message)
    try:
        if vmDetails.get('dataStoreName'):
            dataStore = getVSphereObj(content, [vim.Datastore], vmDetails['dataStoreName'])
        else:
            dataStore = getVSphereObj(content, [vim.Datastore], template.datastore[0].info.name)
        if not dataStore:
            raise
    except:
        message = "Cannot get the dataStore: %s"%vmDetails.get('dataStoreName')
        logging.exception(message)
        raise Exception(message)

    # if None, get the first one
    cluster = getVSphereObj(content, [vim.ClusterComputeResource], vmDetails['clusterName'])
    resourcePool = None
    try:
        if vmDetails.get('resourcePool'):
            resourcePool = getVSphereObj(content, [vim.ResourcePool], vmDetails['resourcePool'])
        else:
            resourcePool = cluster.resourcePool
    except:
        message = "Cannot get the resource Pool: %s"%vmDetails.get('resourcePool')
        logging.exception(message)
        raise Exception(message)
    # set relospec
    reloSpec = vim.vm.RelocateSpec()
    reloSpec.datastore = dataStore
    reloSpec.pool = resourcePool

    # Check whether disk mode is set to thin or thick provision and set the disk property.
    if vmDetails.get('vmDiskDetails'):
        vmDiskDetails = vmDetails.get('vmDiskDetails')
        if vmDiskDetails.get('diskMode') and vmDiskDetails.get('diskMode') == 'thin':
            reloSpec.transform = vim.VirtualMachineRelocateTransformation().sparse
        elif vmDiskDetails.get('diskMode') and vmDiskDetails.get('diskMode') == 'thick':
            reloSpec.transform = vim.VirtualMachineRelocateTransformation().flat
        else:
            logging.warn('Unknown diskmode VM will be provisioned with same disk mode as source.')
    else:
        logging.warn('No diskmode supplied VM will be provisioned with same disk mode as source')


    cloneSpec = vim.vm.CloneSpec()
    cloneSpec.location = reloSpec
    cloneSpec.customization = customSpecVM
    cloneSpec.powerOn = False

    logging.info("Deploying VM with VM name : '%s' from Template: '%s' ", vmDetails['vmName'], templateName)
    logging.info("Datacenter name is : '%s', Datastore name is: '%s',Cluster name is: '%s'",dataCenter.name, dataStore.name,
                 cluster.name)

    task = template.Clone(folder=destFolder, name=vmDetails['vmName'], spec=cloneSpec)
    waitForTask(task, interval, timeout)
    vmObj = getVMByName(serviceInstance, vmDetails.get('vmName', None))
    logging.info('Checking if portgroup has been supplied.')
    if vmDetails.get('portgroup', None):
        logging.info('Configuring VM %s to use portgroup %s' % (vmObj.name, vmDetails['portgroup']))
        addNICToDvSwitch(content, vmObj, vmDetails['portgroup'])
    else:
        logging.info('No portgroup supplied.')
    import common.vmUtils as vmUtil
    vmUtil.resizeVM(vmObj, vmDetails.get('cpuConfig', None), vmDetails.get(
        'vmMemoryConfig', None), vmDetails.get('hddConfig', None))
    eventManager = serviceInstance.content.eventManager
    eventFilterSpec = vim.event.EventFilterSpec()
    eventFilterByEntitySpec = vim.event.EventFilterSpec.ByEntity()
    eventFilterByEntitySpec.entity = vmObj
    eventFilterByEntitySpec.recursion = vim.event.EventFilterSpec.RecursionOption.all
    eventFilterSpec.entity = eventFilterByEntitySpec
    eventCollector = eventManager.CreateCollectorForEvents(eventFilterSpec)
    eventCollector.SetCollectorPageSize(1000)
    events = eventCollector.latestPage
    CustomizationCompletionFlag = 0
    timeCounter = 0
    while CustomizationCompletionFlag == 0:
        logging.info("Waiting for customization spec to apply to VM-%s", vmObj.name)
        for event in events:
            if type(event).__name__ == "vim.event.CustomizationStartedEvent":
                logging.info("Customization started")
            elif type(event).__name__ == "vim.event.CustomizationSucceeded":
                logging.info("Customization Spec applied successfully")
                CustomizationCompletionFlag = 1
                break
            elif(type(event).__name__ == "vim.event.CustomizationSysprepFailed" or type(event).__name__ == \
                    "vim.event.CustomizationUnknownFailure" or type(event).__name__ == \
                    "vim.event.CustomizationNetworkSetupFailed"):
                logging.critical("Customization failed for VM-%s", vmObj.name)
                raise Exception("Customization failed for VM-%s", vmObj.name)
        # EHCINSTALL-1337 - removed the temporary fix added under EHCINSTALL-1079
        eventCollector.SetCollectorPageSize(1000)
        events = eventCollector.latestPage
        time.sleep(constants.CUSTOMIZATION_SPEC_STATUS_CHANGE_INTERVAL)

        # Change Request to use timeout paramter
        # if timeCounter <= constants.DEFAULT_TIMEOUT_SECS:
        if timeCounter <= timeout:
            timeCounter += constants.CUSTOMIZATION_SPEC_STATUS_CHANGE_INTERVAL
        else:
            logging.critical("Time out in waiting for customization spec to apply to VM-%s", vmObj.name)
            raise RuntimeError("Time out in waiting for customization spec to apply to VM-%s", vmObj.name)

    # Waiting for Windows to become interactive
    waitWithTimeout(lambda: vmObj.guest.interactiveGuestOperationsReady == True,
                    'interactive Guest Operation Ready VM-{}'.format(vmObj.name),
                    timeout=constants.INTERACTIVE_GUEST_OPETATION_READY_TIMEOUT)

    logging.info("VM with name : '%s' successfully deployed", vmDetails['vmName'])
    logging.info("Template used is: '%s' ", templateName)
    logging.info("Datacenter name is : '%s', Datastore name is: '%s',Cluster name is: '%s'",dataCenter.name, dataStore.name,
                 cluster.name)

@logDeco.logFunction
def getESXiService(hostSystem, key):
    """
    Description: Get service with key 'key' from 'serviceInstance'.
    Parameters: host: The HostSystem object whose services to get. (OBJECT)
                key: The key of the service to get. (STRING)
    Return: The service if found, else None. (OBJECT)
    """
    logging.info("Searching host %s for service with key %s",
                 hostSystem.summary.config.name, key)
    hostServiceList = hostSystem.configManager.serviceSystem.serviceInfo.service
    for service in hostServiceList:
        if service.key == key:
            logging.info("Found service %s in host %s", key, hostSystem.summary.config.name)
            return service

    logging.info("Could not find service %s in host %s", key, hostSystem.summary.config.name)
    return None

@logDeco.logFunction
def enableESXiService(hostSystem, service):
    """
    Description: Enable 'service' on host 'serviceInstance'.
    Parameters: host: The HostSystem object on which to enable the service. (OBJECT)
                service: The service to enable. (OBJECT)
    Return: Whether the enable action was actually performed. (BOOL)
    """
    logging.info("Enabling service %s on host %s.",
                 service.key, hostSystem.summary.config.name)
    alreadyEnabled = service.running
    if alreadyEnabled:
        logging.info("Service %s already running on host %s.",
                     service.key, hostSystem.summary.config.name)
        return False
    serviceSystem = hostSystem.configManager.serviceSystem
    serviceSystem.StartService(service.key)
    logging.info("Enabled service %s on host %s.", service.key, hostSystem.summary.config.name)
    return True

@logDeco.logFunction
def disableESXiService(hostSystem, service):
    """
    Description: Disable 'service' on host 'serviceInstance'.
    Parameters: host: The HostSystem object on which to disable the service. (OBJECT)
                service: The service to disable. (OBJECT)
    """
    serviceSystem = hostSystem.configManager.serviceSystem
    serviceSystem.StopService(service.key)
    logging.info("Disabled service %s on host %s.", service.key, hostSystem.summary.config.name)

@commonExceptionHandler()
def enableSSHByCluster(vCenterDict, clusterName, sshDict):
    """
    Description: Enable SSH session each ESXi host in cluster, so that esxcli command can be excuted on host
    :param vCenterDict: vCenter info (DICT)
            vCenterDict['host']: IP or FQDN of vCenter (STRING)
            vCenterDict['username']: username of vCenter (STRING)
            vCenterDict['password']: password of vCenter (STRING)
    :param clusterName: Cluster name (STRING)
    :param sshDict: ESXi host SSH credential info (DICT)
            sshDict['sshUsername']: The username for connecting to the host through SSH.
            sshDict['sshPassword']: The password for connecting to the host through SSH.
    :return: A dict 'resultDic' with the following keys: (DICT)
        {'status':True, 'hostList': hostList} or {'status':False, 'message': error message}
        retDict['status']: The overall status of the validation. (BOOL)
        retDict['hostList']: Incidating the host list in cluster
    """
    resultDic = {}
    logging.info("Start enableSSHByCluster for Cluster '%s'", clusterName)
    si = connectToVcenter(vCenterDict['host'], vCenterDict['username'], vCenterDict['password'])
    logging.info("Start getting ESXi hosts for Cluster '%s'", clusterName)
    hosts = getHostsByCluster(si, clusterName)
    logging.info("Successfully get ESXi hosts for Cluster '%s'", clusterName)
    disconnectFromVcenter(si)

    resultDic['hostList'] = hosts
    resultDic['status'] = True

    for host in hosts:
        # Do not use getESXiHost as we need disconnect from vcenter after each iteration
        sih = connectToVcenter(host, sshDict['sshUsername'], sshDict['sshPassword'])
        hostSystem = sih.content.rootFolder.childEntity[0].hostFolder.childEntity[0].host[0]
        logging.info("Getting the HostSystem object for host %s using username %s", host, sshDict['sshUsername'])
        # SSH validation
        sshService = getESXiService(hostSystem, constants.ESXI_HOST_SSH_SERVICE_KEY)
        if not sshService:
            msg = "Validation Failed: Could not find SSH service on host '%s'"%host
            logging.critical(msg)
            resultDic['status'] = False
            resultDic['message'] = msg
            return resultDic
        logging.info("Ensuring that SSH service is running on host '%s'", host)
        sshEnabled = enableESXiService(hostSystem, sshService)
        # if enable failed, exception will be thrown
        if sshEnabled:
            logging.info("Enabled SSH service for host: '%s'", host)
        disconnectFromVcenter(sih)
    return resultDic

@commonExceptionHandler()
def disableSSHByCluster(vCenterDict, clusterName, sshDict):
    """
    Description: Disable SSH session each ESXi host in cluster, for security reason.
    vCenter Infomation is needed as we might fail in enableSSHByCluster but we need get host from vcenter, 
    :param vCenterDict: vCenter info (DICT)
            vCenterDict['host']: IP or FQDN of vCenter (STRING)
            vCenterDict['username']: username of vCenter (STRING)
            vCenterDict['password']: password of vCenter (STRING)
    :param clusterName: Cluster name (STRING)
    :param sshDict: ESXi host SSH credential info (DICT)
            sshDict['sshUsername']: The username for connecting to the host through SSH.
            sshDict['sshPassword']: The password for connecting to the host through SSH.
    :return: A dict 'resultDic' with the following keys: (DICT)
        {'status':True, 'message': success message} or {'status':False, 'message': error message}
        retDict['status']: The overall status of the validation. (BOOL)
    """
    returnResult = {'status':True, 'message':'success'}
    logging.info("Start disableSSHByCluster for Cluster '%s'", clusterName)
    si = connectToVcenter(vCenterDict['host'], vCenterDict['username'], vCenterDict['password'])
    logging.info("Start getting ESXi hosts for Cluster '%s'", clusterName)
    hosts = getHostsByCluster(si, clusterName)
    logging.info("Successfully get ESXi hosts for Cluster '%s'", clusterName)
    disconnectFromVcenter(si)

    for host in hosts:
        sih = connectToVcenter(host, sshDict['sshUsername'], sshDict['sshPassword'])
        hostSystem = sih.content.rootFolder.childEntity[0].hostFolder.childEntity[0].host[0]
        logging.info("Getting the HostSystem object for host %s using username %s",  host, sshDict['sshUsername'])
        # SSH validation
        sshService = getESXiService(hostSystem, constants.ESXI_HOST_SSH_SERVICE_KEY)
        if not sshService:
            message = "Validation Failed: Could not find SSH service on host '%s'" % host
            logging.critical(message)
            return {'status': False, 'message': message}
        disableESXiService(hostSystem, sshService)
        disconnectFromVcenter(sih)
    return returnResult

@logDeco.logFunction
def getESXiHost(hostname, username, password):
    """
    Description: Get the HostSystem object for ESXi host 'hostname'.
    Parameters: hostname: The IP/FQDN of the host to get. (STRING)
                username: The username to connect to the host. (STRING)
                password: The password to connect to the host. (STRING)
    Return: The HostSystem object representing hostname. (OBJECT)
    """
    serviceInstance = connectToVcenter(hostname, username, password)
    hostSystem = serviceInstance.content.rootFolder.childEntity[0].hostFolder.childEntity[0].host[0]
    logging.info("Getting the HostSystem object for host %s using username %s", hostname, username)
    return hostSystem

@logDeco.logFunction
def gracefulRestartVM(vCenterDict, vmDict):
    """
    Description: Function gracefully Restart VM.
    parameters: vCenterDict: vCenter info(DICT)
                             host: vCenter IP(STRING)
                             user: User namefor vCenter(STRING)
                             password: Password for vCenter(STRING)
                vmDict     : Guest VM info(DICT)
                             vmname: Guest VM Name(STRING)

    """

    logging.info("Restarting VM named %s.....", vmDict['vmname'])
    serviceInstance = connectToVcenter(vCenterDict['host'], vCenterDict['user'], vCenterDict['password'])

    # Getting the VM Object by Name
    logging.debug('Getting the VM Obj for the remote VM %s', vmDict['vmname'])
    vm = getVMByName(serviceInstance, vmDict['vmname'])
    logging.info('VM Obj found for the VM %s', vmDict['vmname'])

    gracefulShutDownVM(vm)
    gracefulStartVM(vm)

@logDeco.logFunction
def destroyVM(vCenterObj, vmName):
    """
     Description: Destroy the VM
     Parameters: vCenterObj: vCenter object(OBJ)
                 vmName: Name of the vCenter
     Return: None
     """
    try:
        vmObj = getVMByName(vCenterObj, vmName)
    except Exception as ex:
        logging.info('Unable to locate VirtualMachine named %s', vmName)
        return None
    powerOffVM(vmObj)
    destroyVM = vmObj.Destroy_Task()
    waitForTask(destroyVM)
    logging.info("Destroying the VM named %s", vmName)

@logDeco.logFunction
def addLicenseToVCenter(serviceInstance, licenseKey):
    """
    Description: add a license into vCenter
    :param serviceInstance: connection object to vCenter server
    :param licenseKey: a license key string
    :return: True or False
    """
    licenseManager = _getLicenseManager(serviceInstance)
    try:
       licenseInfo = licenseManager.AddLicense(licenseKey)
    except Exception as ex:
        logging.error("Failed to add license to vCenter: %s"%ex.message)
        return False
    return licenseKey == licenseInfo.licenseKey

@logDeco.logFunction
def validateAddLicenseToVCenter(serviceInstance, licenseKey):
    """
    Description: validate a license key whether imported into vCenter or not
    :param serviceInstance: connection object to vCenter server
    :param licenseKey: the license key to be validated
    :return: True or False
    """
    licenseManager = _getLicenseManager(serviceInstance)
    try:
        licensesExisting = [licenseInfo.licenseKey for licenseInfo in licenseManager.licenses]
        return licenseKey in licensesExisting
    except Exception as ex:
        message = 'Failed to validate the added license whether exists in vCenter.%s'%ex.message
        logging.error(message)
        return False

@logDeco.logFunction
def updateLicenseAssignmentOnVCenter(serviceInstance, licenseKey, licenseAssignmentDisplayName):
    """
    Description: update license assignment on vCenter
    :param serviceInstance: connection object to vCenter server
    :param licenseKey: the license key to be assigned
    :param licenseAssignmentDisplayName: display name of a license assignment
    :return: True or False
    """
    licenseAssignmentManager = _getLicenseAssignmentManager(serviceInstance)
    targetLicenseAssignments = _getLicenseAssignmentsByDisplayName(licenseAssignmentManager,
                                                                  licenseAssignmentDisplayName)
    if len(targetLicenseAssignments) == 0:
        return False
    result = True
    for assignment in targetLicenseAssignments:
        try:
            licenseInfo = licenseAssignmentManager.UpdateAssignedLicense(assignment.entityId, licenseKey)
            result = result and licenseKey == licenseInfo.licenseKey
        except Exception as ex:
            message = 'Failed to update license assignment on vCenter. %s'%ex.message
            logging.exception(message)
    return result

@logDeco.logFunction
def validateUpdateLicenseAssignmentOnVCenter(serviceInstance, licenseKey, licenseAssignmentDisplayName):
    """
    Description: validate license assignment with given license key and display name on vCenter
    :param serviceInstance: connection object to vCenter server
    :param licenseKey: the license key to be assigned
    :param licenseAssignmentDisplayName: display name of a license assignment
    :return: True or False
    """
    licenseAssignmentManager = _getLicenseAssignmentManager(serviceInstance)
    targetLicenseAssignments = _getLicenseAssignmentsByDisplayName(licenseAssignmentManager,
                                                                  licenseAssignmentDisplayName)
    if len(targetLicenseAssignments) == 0:
        return False
    result = True
    for assignment in targetLicenseAssignments:
        result = result and licenseKey == assignment.assignedLicense.licenseKey
    return result


@logDeco.logFunction
def _getLicenseManager(serviceInstance):
    """
    Description: get LicenseManager of a vCenter
    :param serviceInstance: connection object to vCenter server
    :return: LicenseManager object
    """
    try:
        content = serviceInstance.RetrieveContent()
        return content.licenseManager
    except Exception as ex:
        message = 'Failed to get LicenseManger. %s'%ex.message
        logging.exception(message)

@logDeco.logFunction
def _getLicenseAssignmentManager(serviceInstance):
    """
    Description: get LicenseAssignmentManager of a vCenter
    :param serviceInstance: connection object to vCenter server
    :return: LicenseAssignmentManager object
    """
    try:
        return _getLicenseManager(serviceInstance).licenseAssignmentManager
    except Exception as ex:
        message = 'Failed to get LicenseAssignmentManger. %s'%ex.message
        logging.exception(message)

@logDeco.logFunction
def _getLicenseAssignmentsByDisplayName(licenseAssignmentManager, licenseAssignmentDisplayName):
    """
    Description: find licenseAssignments by display name
    :param licenseAssignmentManager: license assignment manager
    :param licenseAssignmentDisplayName: display name of a license assignment
    :return: a list of licenseAssignments that matches display name given
    """
    try:
        allLicenseAssignments = licenseAssignmentManager.QueryAssignedLicenses()
        assignments = [assignment
                  for assignment in allLicenseAssignments
                  if assignment.entityDisplayName == licenseAssignmentDisplayName]
        logging.info('Found %s license assignments by displayName=%s'%(len(assignments), licenseAssignmentDisplayName))
        return assignments
    except Exception as ex:
        message = 'Failed to get LicenseAssignment by displayName. %s'%ex.message
        logging.exception(message)
        return []

def revertVmToSnapshot(vmObj, snapshotName):
    """
    description: This funciton is used to revert VM to a specific snapshot
    :param vmObj: virtual machine Object (OBJECT)
    :param snapshotName: snapshot's name(STRING)
    :return: True or False
    """
    try:
        logging.info("Start to restore target VM to snaoshot: {}".format(snapshotName))
        if vmObj.snapshot is not None:
            snapshotTrees = vmObj.snapshot.rootSnapshotList
            if snapshotTrees:
                vm_snapshot = findSnapshotByName(snapshotTrees, snapshotName)
            else:
                logging.info("Snapshot trees does not exist.")
                return False
        else:
            logging.info("Target VM does not have snapshot.")
            return False
        if vm_snapshot is None:
            logging.error("Didn't find target snapshot {}.".format(snapshotName), True)
            raise AssertionError("Didn't find target snapshot {}.".format(snapshotName))
        task = vm_snapshot.RevertToSnapshot_Task()
        waitForTask(task)
        return True
    except Exception as e:
        logging.exception("Exception: {0} occurs when trying to restore target VM to snapshot: {1}".format(e, snapshotName))
        return False


@logDeco.logFunction
def findSnapshotByName(snapshotTrees, snapshotName):
    """
    description: This funciton is used to find a specific snapshot
    :param snapshotTrees: Data for the entire set of snapshots for one virtual machine.(Object)
    :param snapshotName: snapshot's name (STRING)
    :return: snapshot object or None
    """
    try:
        logging.info("Start to find given snapshot: {}".format(snapshotName))
        snapshot = None
        if snapshotTrees:
            for tree in snapshotTrees:
                if tree.name == snapshotName:
                    logging.info("Found snapshot: {}".format(snapshotName))
                    snapshot = tree.snapshot
                    break
                elif tree.childSnapshotList:
                    snapshot = findSnapshotByName(tree.childSnapshotList, snapshotName)
                    if snapshot:
                        logging.info("Found snapshot: {}".format(snapshotName))
                        break
        else:
            logging.info("Snapshot trees does not provided.")
    except Exception as e:
        logging.exception("Exception: {0} occurs when trying to find snapshot: {1}".format(e, snapshotName))
        snapshot = None
    finally:
        return snapshot


@logDeco.logFunction
def findVMByInventoryPath(serviceInstance, inventoryPath):
    """
    Description: find a VM or Host by inventory path from vCenter
    :param serviceInstance: vCenter connection object
    :param inventoryPath: Inventory path of a VM
        ['datacenter']: datacenter name that contains the VM(String),
        ['vmName']: VM name(String),
        ['folderPath']:(optional)Folder path that contains the VM(String)
    :return: VM object
    """
    try:
        path = _buildInventoryPath(inventoryPath)
        searchIndex = serviceInstance.content.searchIndex
        vm = searchIndex.FindByInventoryPath(path)
        if vm is not None:
            logging.info("Found VM by inventory path[%s]"%path)
        return vm
    except Exception as ex:
        message="Failed to find VM. %s"%ex.message
        logging.exception(message)
        return None


@logDeco.logFunction
def find_vm_by_uuid(service_instance, uuid):
    """
    Description: find a VM by uuid
    :param service_instance: vCenter connection object
    :param uuid:  UUID of VM       
    :return: VM object if Found, otherwise None
    """
    try:
        logging.info("Finding VM by uuid: {0}".format(uuid))
        searchIndex = service_instance.content.searchIndex
        vm = searchIndex.FindByUuid(None, uuid, True, True)
        if vm is not None:
            logging.info("Found VM: {0} for uuid: {1}".format(vm.name, uuid))
        return vm
    except Exception as ex:
        logging.exception('Exception occurred while finding VM,'
                          ' error: {}'.format(ex))


@logDeco.logFunction
def _buildInventoryPath(inventoryPathDict):
    """
    Build the inventory path of a VM
    :param inventoryPathDict: Inventory path of a VM
    ['datacenter']: datacenter name that contains the VM(String),
    ['vmName']: VM name(String),
    ['folderPath']:(optional)Folder path that contains the VM(String)
    :return: The Inventory path of a VM(String)
    """
    keys = inventoryPathDict.keys()
    if 'datacenter' not in keys or 'vmName' not in keys:
        message = 'datacenter and VM name are required in input Dictionary. please check.'
        logging.error('Invalid input. %s' % message)
        raise RuntimeError(message)
    seprator = '/'
    inventoryPath = '{0}{1}vm{2}'.format(inventoryPathDict['datacenter'], seprator, seprator)
    if 'folderPath' in keys:
        inventoryPath += inventoryPathDict['folderPath']
        inventoryPath += seprator
    slashRepresenter = '%2f'
    vmName = inventoryPathDict['vmName'].replace(seprator, slashRepresenter)
    inventoryPath += vmName
    inventoryPath = inventoryPath.replace('//', seprator)#defensive for some negative input
    logging.info("Generated Inventory Path=%s"%inventoryPath)
    return inventoryPath

@logDeco.logFunction
def getResourcePoolInClusterByName(serviceInstance, clusterName, resourcePoolName):
    """
    Description: get the ResourcePool object by name under the root folder of the given cluster,
    any sub nested ResourcePool will be ignored.
    :param serviceInstance: vCenter connection object(Object)
    :param clusterName: name of a cluster(String)
    :param resourcePoolName: name of a resource pool
    :return: ResourcePool Obj or None if not found
    """
    content = serviceInstance.RetrieveContent()
    container = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.ResourcePool], True)
    for resourcePool in container.view:
        if resourcePool.name == resourcePoolName and resourcePool.owner.name == clusterName and resourcePool.parent.name == ROOT_RESOURCE_POOL_NAME:
            return resourcePool
    return None


def _getExtensionManager(serviceInstance):
    """
    Description: get ExtensionManager
    :param serviceInstance: vCenter connection object(Object)
    :return: ExtensionManager(Object)
    """
    content = serviceInstance.RetrieveContent()
    extensionManager = content.extensionManager
    return extensionManager


@logDeco.logFunction
def registerExtension(serviceInstance, extension):
    """
    Description: register an extension to vCenter web client
    :param serviceInstance: vCenter connection object(Object)
    :param extension: extension object(Object)
    """

    extensionManager = _getExtensionManager(serviceInstance)
    if validateExtension(serviceInstance, extension.key):
        logging.info("Extension key %s already exists, no need register.", extension.key)
        return
    else:
        extensionManager.RegisterExtension(extension)
        logging.info("Register extension %s Successfully", extension.key)

@logDeco.logFunction
def getDataStoreIdByName(serviceInstance, dsname):
    dc, ds = _getDatacenterDatastore(serviceInstance, dsname)
    if not ds is None and not ds._moId is None:
        return ds._moId.encode('utf-8')
    return None

@logDeco.logFunction
def getNetworkIdAndHostIdsByName(serviceInstance, networkName, hostName):
    for dc in serviceInstance.content.rootFolder.childEntity:
        if not dc.network is None:
            return _findNetworkAndHostIdViaNetworks(dc.network, networkName, hostName)
    return None, None

@logDeco.logFunction
def _findNetworkAndHostIdViaNetworks(networks, networkName, hostName):
    for network in networks:
        networkId, hostId = _findNetworkAndHostId(network, networkName, hostName)
        if not networkId is None:
            return networkId, hostId

@logDeco.logFunction
def _findNetworkAndHostId(network, networkName, hostName):
    if network.name == networkName and not network._moId is None:
        host_id = None
        if not network.host is None:
            host_id = _findNetworkAndHostIdViaHosts(network.host, hostName)
        return network._moId.encode('utf-8'), host_id
    return None, None

@logDeco.logFunction
def _findNetworkAndHostIdViaHosts(hosts, hostName):
    for host in hosts:
        if not host._moId is None and host.name == hostName:
            host_id = host._moId.encode('utf-8')
            return host_id
    return None

@logDeco.logFunction
def getExtensionObjByKey(serviceInstance, extensionKey):
    """
          Description: register an extension to vCenter web client
          :param serviceInstance: vCenter connection object(Object)
          :param extension: extension object(Object)
          return: (Boolean)
          """
    extensionManager = _getExtensionManager(serviceInstance)
    existingExtensions = extensionManager.extensionList
    for extension in existingExtensions:
        if extension.key==extensionKey:
            return extension
    return None

@logDeco.logFunction
def validateExtension(serviceInstance, extensionKey):
    """
        Description: register an extension to vCenter web client
        :param serviceInstance: vCenter connection object(Object)
        :param extension: extension object(Object)
        return: (Boolean)
        """
    extensionManager = _getExtensionManager(serviceInstance)
    existingExtensions = extensionManager.extensionList
    existingKeys = [ext.key for ext in existingExtensions]
    if extensionKey in existingKeys:
        return True
    return False

@logDeco.logFunction
def unregisterExtension(serviceInstance, extensionKey):
    """
     Description: unegister an extension to vCenter web client
     :param serviceInstance: vCenter connection object(Object)
     :param extension: extension object(Object) 
     
     :return: (Boolean) 
     """

    extensionManager = _getExtensionManager(serviceInstance)

    if validateExtension(serviceInstance, extensionKey):
        unregisterResult = extensionManager.UnregisterExtension(extensionKey)
        logging.info("Unregister extension %s is successful..." % extensionKey)

        return True if unregisterResult is None else False
    return True

@logDeco.logFunction
def getClusterIdByName(serviceInstance, clusterName):
    """
    Description: Get Cluster Id by its name
    :param serviceInstance: service instance (get from connectTovCenter()) [OBJECT]
    :param clusterName: cluster name [STRING]
    :return: cluster Id [STRING]
    """
    try:
        content = serviceInstance.RetrieveContent()
        clusterObj = getVSphereObj(content, [vim.ClusterComputeResource], clusterName)
        if not clusterObj:
            logging.info('Found no object for %s ' % clusterName)
            return None
        return str(clusterObj._moId)
    except Exception as e:
        logging.exception('Error occurred when getting cluster id for{0}, {1}'.format(clusterName, e.message))
        raise

@logDeco.logFunction
def getHostsByCluster(serviceInstance, clusterName):
    """
    Description: Get ESXi host list from Cluster
    :param serviceInstance: service instance (get from connectTovCenter()) [OBJECT]
    :param clusterName: cluster name [STRING]
    :return: Host FQDN/IP List [LIST]
    """
    try:
        hostList = []
        content = serviceInstance.RetrieveContent()
        clusterObj = getVSphereObj(content, [vim.ClusterComputeResource], clusterName)
        if not clusterObj:
            logging.info('Found no Cluster object for %s ' % clusterName)
            return None
        for hostObj in clusterObj.host:
            logging.info('Found ESXi host %s' % hostObj.name)
            hostList.append(hostObj.name)
        return hostList
    except Exception as e:
        logging.exception('Error occurred when getting hosts from cluster {0}, {1}'.format(clusterName, e.message))
        raise


@logDeco.logFunction
def getHostObjectByHostName(serviceInstance, clusterName, hostName):
    """
    Description: Get ESXi host from Cluster by hostName
    :param serviceInstance: service instance (get from connectTovCenter()) [OBJECT]
    :param clusterName: cluster name [STRING]
    :param hostName: target host's name (STRING)
    :return: List of vim.HostSystem [LIST]
    """
    try:
        content = serviceInstance.RetrieveContent()
        clusterObj = getVSphereObj(content, [vim.ClusterComputeResource], clusterName)
        if not clusterObj:
            logging.info('Found no Cluster object for %s ' % clusterName)
            return None
        for hostObj in clusterObj.host:
            if hostName == hostObj.name:
                logging.error('Host %s found on cluster: %s' % (hostName, clusterName))
                return hostObj
        logging.error('Host %s not found on cluster: %s' % (hostName, clusterName))
        return None
    except Exception as e:
        logging.exception('Error occurred when getting hosts from cluster {0}, {1}'.format(clusterName, e.message))
        raise


@logDeco.logFunction
def getHostObjectsByCluster(serviceInstance, clusterName):
    """
    Description: Get ESXi host list from Cluster
    :param serviceInstance: service instance (get from connectTovCenter()) [OBJECT]
    :param clusterName: cluster name [STRING]
    :return: List of vim.HostSystem [LIST]
    """
    try:
        logging.info('Start to retrieve host list from cluster: %s', clusterName)
        hostList = []
        content = serviceInstance.RetrieveContent()
        clusterObj = getVSphereObj(content, [vim.ClusterComputeResource], clusterName)
        if not clusterObj:
            logging.info('Found no Cluster object for %s ' % clusterName)
            return None
        for hostObj in clusterObj.host:
            hostList.append(hostObj)
        return hostList
    except Exception as e:
        logging.exception('Error occurred when getting hosts from cluster {0}, {1}'.format(clusterName, e.message))
        raise


@logDeco.logFunction
def hostEnterMaintenanceMode(hostSystem, vsanMode=vim.vsan.host.DecommissionMode.ObjectAction.ensureObjectAccessibility,task=None):
    """
    Description: function to enter the maintenance mode for the host
    :param hostSystem: ESXi host object [vim.HostSystem]
    :param vsanMode: vsan decommission object action [vim.vsan.host.DecommissionMode.ObjectAction] Optional
    :return: True or False [bool]
    """

    if hostSystem.runtime.connectionState != vim.HostSystem.ConnectionState.connected:
        logging.info("Host: %s is not connected, do nothing" % hostSystem.name)
        return True
    if hostSystem.runtime.inMaintenanceMode:
        logging.info("Already in maintenance mode for host: %s, no action needed." % hostSystem.name)
        return True
    if task:
        logging.info("Wait for previous maintenance mode task to complete")
        _waitForMaintenaceModeTask(task)
        if hostSystem.runtime.inMaintenanceMode:
            logging.info("Succeeded to enter maintenance mode for host: %s" % hostSystem.name)
            return True
        else:
            logging.info("Failed to enter maintenance mode for host: %s" % hostSystem.name)
            return False
    logging.info("Start to enter maintenance mode for host: %s" % hostSystem.name)
    decommisionMode = vim.vsan.host.DecommissionMode()
    decommisionMode.objectAction = vim.vsan.host.DecommissionMode.ObjectAction.ensureObjectAccessibility
    if vsanMode != vim.vsan.host.DecommissionMode.ObjectAction.ensureObjectAccessibility:
        if vsanMode == vim.vsan.host.DecommissionMode.ObjectAction.evacuateAllData or vsanMode == vim.vsan.host.DecommissionMode.ObjectAction.noAction:
            decommisionMode.objectAction = vsanMode
        else:
            logging.warn("Unspported vsan decommission mode %s, ignored", vsanMode)
    logging.info("decommisionMode is %s", decommisionMode.objectAction)
    mainSpec = vim.host.MaintenanceSpec()
    mainSpec.vsanMode  = decommisionMode
    task = hostSystem.EnterMaintenanceMode(constants.DEFAULT_TIMEOUT_SECS_HOST_ENTER_MAINTENANCE_MODE, maintenanceSpec=mainSpec)
    waitForTask(task, timeout=constants.DEFAULT_TIMEOUT_SECS_HOST_ENTER_MAINTENANCE_MODE)
    if hostSystem.runtime.inMaintenanceMode:
        logging.info("Succeeded to enter maintenance mode for host: %s" % hostSystem.name)
        return True
    else:
        logging.info("Failed to enter maintenance mode for host: %s" % hostSystem.name)
        return False


@logDeco.logFunction
def _waitForMaintenaceModeTask(task):
    try:
        if task.info:
            logging.info("Task is still progressing")
    except Exception as e:
        logging.info("Task has expired or completed .")
        return
    waitForTask(task, timeout=constants.DEFAULT_TIMEOUT_SECS_HOST_ENTER_MAINTENANCE_MODE)

@logDeco.logFunction
def hostExitMaintenanceMode(hostSystem):
    """
        Description: function to exit the maintenance mode for the host
        :param hostSystem: ESXi host object [vim.HostSystem]
        :return: True or False [bool]
    """
    if hostSystem.runtime.connectionState != vim.HostSystem.ConnectionState.connected:
        logging.info("Host: %s is not connected, do nothing" % hostSystem.name)
        return True
    if not hostSystem.runtime.inMaintenanceMode:
        logging.info("Currently not in maintenance mode for host: %s, no action needed." % hostSystem.name)
        return True
    logging.info("Start to exit maintenance mode for host: %s" % hostSystem.name)
    task = hostSystem.ExitMaintenanceMode(constants.DEFAULT_TIMEOUT_SECS)
    waitForTask(task)
    if not hostSystem.runtime.inMaintenanceMode:
        logging.info("Succeeded to exit maintenance mode for host: %s" % hostSystem.name)
        return True
    else:
        logging.info("Failed to exit maintenance mode for host: %s" % hostSystem.name)
        return False


@logDeco.logFunction
def rebootNeededForHost(hostSystem):
    """
    Description: function to check if reboot needed for the host
    :param hostSystem: ESXi host object [vim.HostSystem]
    :return: True or False [bool]
    """
    logging.info('Checking if reboot needed for host: %s' % hostSystem.name)
    return hostSystem.summary.rebootRequired


@logDeco.logFunction
def rebootHost(hostSystem):
    """
    Description: function to initiate the reboot action for host
    :param hostSystem: ESXi host object [vim.HostSystem]
    :return: True or False
    """
    logging.info('Start to reboot host: %s' % hostSystem.name)
    task = hostSystem.Reboot(False)
    waitForTask(task)
    logging.info('Succeeded to trigger the reboot operation on host: %s' % hostSystem.name)
    return True


@logDeco.logFunction
def waitSometimeForRebootHappened(hostSystem, interval=DEFAULT_INTERVAL_SECS, timeout=DEFAULT_TIMEOUT_SECS_HOST_REBOOT):
    """
    Description: loop checking if this host rebooting is started
    :param hostSystem: ESXi host object [vim.HostSystem]
    :param interval: check interval, in seconds [int]
    :param timeout: totle timeout, in seconds [int]
    :return: True / False [bool]
    """
    logging.info('Wait some time for the reboot to start for host: %s' % hostSystem.name)
    logging.debug('Current connectionState: %s' % hostSystem.runtime.connectionState)
    totalWaitTime = 0
    while hostSystem.runtime.connectionState != vim.HostSystem.ConnectionState.notResponding and totalWaitTime < timeout:
        logging.debug('Current connectionState: %s' % hostSystem.runtime.connectionState)
        logging.debug('rebooting not started yet, keep waiting: %s for %ds', hostSystem.name, interval)
        time.sleep(interval)
        totalWaitTime += interval
    if not totalWaitTime < timeout:
        message = 'Timed out waiting for host reboot to start'
        logging.critical(message)
        raise RuntimeError(message)
    logging.info('Host: %s reboot is started, will poll to check if host is back' % hostSystem.name)
    return True


@logDeco.logFunction
def pollRebootedHost(hostSystem, interval=DEFAULT_INTERVAL_SECS, timeout=DEFAULT_TIMEOUT_SECS):
    """
    Description: poll host to see it's connection state
    :param hostSystem: ESXi host object [vim.HostSystem]
    :param interval: check interval, in seconds [int]
    :param timeout: totle timeout, in seconds [int]
    :return: True / False [bool]
    """
    logging.info('Start to polling if host: %s is back from reboot' % hostSystem.name)
    logging.debug('Current connectionState: %s' % hostSystem.runtime.connectionState)
    logging.debug('Current overallStatus: %s' % hostSystem.summary.overallStatus)
    totalWaitTime = 0
    while not (hostSystem.runtime.connectionState == vim.HostSystem.ConnectionState.connected) \
            and totalWaitTime < timeout:
        logging.debug('Current connectionState: %s' % hostSystem.runtime.connectionState)
        logging.debug('Current overallStatus: %s' % hostSystem.summary.overallStatus)
        logging.debug('waiting for reboot host: %s for %ds', hostSystem.name, interval)
        time.sleep(interval)
        totalWaitTime += interval
    if not totalWaitTime < timeout:
        message = 'Timed out waiting for host reboot to complete'
        logging.critical(message)
        raise RuntimeError(message)
    logging.info('Host: %s is back and in Green Status now' % hostSystem.name)
    return True

@logDeco.logFunction
def migrateVM(vmObj, hostSystem):
    """
    Description: migrate VM to another host
    :param vmObj: virtual machine object [object]
    :param hostSystem: ESXi host object [vim.HostSystem]
    :return: True / False [bool]
    """
    logging.info("Start to migrate VM: %s to host: %s" % (vmObj.name, hostSystem.name))
    movePriority = vim.VirtualMachine.MovePriority.highPriority
    task = vmObj.Migrate(priority=movePriority, host=hostSystem)
    waitForTask(task)
    if vmObj.runtime.host.name == hostSystem.name:
        logging.info("Succeeded to migrate VM: %s to host: %s" % (vmObj.name, hostSystem.name))
        return True
    else:
        logging.info("Failed to migrate VM: %s to host: %s" % (vmObj.name, hostSystem.name))
        return False


@logDeco.logFunction
def getEsxiHostIdByName(serviceInstance, esxiHostName):
    """
    Description: Get Cluster Id by its name
    :param serviceInstance: service instance (get from connectTovCenter()) [OBJECT]
    :param esxiHostName: ESXI host name [STRING]
    :return: ESXI host Id [STRING]
    """
    try:
        content = serviceInstance.RetrieveContent()
        esxiHostObj = getVSphereObj(content, [vim.HostSystem], esxiHostName)
        if not esxiHostObj:
            logging.info('Found no host object for %s ' % esxiHostName)
            return None
        return str(esxiHostObj._moId)
    except Exception as e:
        logging.exception('Error occurred when getting host id for{0}, {1}'.format(esxiHostName, e.message))
        raise


@logDeco.logFunction
def getDatatoreIdByName(serviceInstance, datastoreName):
    """
    Description: Get Cluster Id by its name
    :param serviceInstance: service instance (get from connectTovCenter()) [OBJECT]
    :param datastoreName: datastore name [STRING]
    :return: datastore Id [STRING]
    """
    try:
        content = serviceInstance.RetrieveContent()
        datastoreObj = getVSphereObj(content, [vim.Datastore], datastoreName)
        if not datastoreObj:
            logging.info('Found no datastore object for %s ' % datastoreName)
            return None
        return str(datastoreObj._moId)
    except Exception as e:
        logging.exception('Error occurred when getting datastore id for{0}, {1}'.format(datastoreName, e.message))
        raise


@logDeco.logFunction
def getVDSIdByName(serviceInstance, vdsName):
    """
    Description: Get distributed switch Id by its name
    :param serviceInstance: service instance (get from connectTovCenter()) [OBJECT]
    :param vdsName: distributed switch name [STRING]
    :return: distributed switch Id [STRING]
    """
    try:
        content = serviceInstance.RetrieveContent()
        vdsObj = getVSphereObj(content, [vim.dvs.VmwareDistributedVirtualSwitch], vdsName)
        if not vdsObj:
            logging.info('Found no vds object for %s ' % vdsName)
            return None
        return str(vdsObj._moId)
    except Exception as e:
        logging.exception('Error occurred when getting vds id for{0}, {1}'.format(vdsName, e.message))
        raise


@logDeco.logFunction
def getStandardSwitchIdByName(serviceInstance, stdSwitchName):
    """
    Description: Get standard switch Id by its name
    :param serviceInstance: service instance (get from connectTovCenter()) [OBJECT]
    :param stdSwitchName: standard switch name [STRING]
    :return: switch Id [STRING]
    """
    try:
        content = serviceInstance.RetrieveContent()
        stdSwitchObj = getVSphereObj(content, [vim.Network], stdSwitchName)
        if not stdSwitchObj:
            logging.info('Found no standard switch object for %s ' % stdSwitchName)
            return None
        return str(stdSwitchObj._moId)
    except Exception as e:
        logging.exception('Error occurred when getting standard switch id for{0}, {1}'.format(
            stdSwitchName, e.message))
        raise

@logDeco.logFunction
def getVdsPortGroupIdByName(serviceInstance, portGroupName):
    """
    Description: Get distributed switch port group Id by its name
    :param serviceInstance: service instance (get from connectTovCenter()) [OBJECT]
    :param portGroupName: port group name [STRING]
    :return: port group Id [STRING]
    """
    try:
        content = serviceInstance.RetrieveContent()
        portGroupObj = getVSphereObj(content, [vim.dvs.DistributedVirtualPortgroup], portGroupName)
        if not portGroupObj:
            logging.info('Found no port group object for %s ' % portGroupName)
            return None
        return str(portGroupObj._moId)
    except Exception as e:
        logging.exception('Error occurred when getting port group id for{0}, {1}'.format(
            portGroupName, e.message))
        raise


@logDeco.logFunction
def getDvsManager(serviceInstance):
    """
    Description: get dvSwitchManager
    :param serviceInstance: vCenter connection object(Object)
    :return: dvSwitchManager
    """
    return serviceInstance.content.dvSwitchManager


@logDeco.logFunction
def getVDSBackupConfigs(serviceInstance, vds, isPortgroupsIncluded=True):
    """
    Description: get Backup Config objects for VDS
    :param serviceInstance: vCenter connection object(Object)
    :param vds: VDS object(Object)
    :param isPortgrousIncluded: whether to include PortGroups(Boolean)
    :return: Backup Config objects(List)
    """
    logging.info("Starting to get VDS backup config objects.")
    selectionSet = []

    dvsSelection = vim.dvs.DistributedVirtualSwitchSelection()
    dvsSelection.dvsUuid = vds.uuid

    selectionSet.append(dvsSelection)

    if isPortgroupsIncluded:
        portGroupKeys = [portGroup.key for portGroup in vds.portgroup]
        pgSelection = vim.dvs.DistributedVirtualPortgroupSelection()
        pgSelection.dvsUuid = vds.uuid
        pgSelection.portgroupKey = portGroupKeys

        selectionSet.append(pgSelection)

    dvsManager = getDvsManager(serviceInstance)
    task = dvsManager.DVSManagerExportEntity_Task(selectionSet)
    timeCount = 0
    while task.info.state == vim.TaskInfo.State.running:
        logging.debug('VDS Backup is running, wait {0} more seconds.'.format(BACKUP_TASK_INTERVAL))
        time.sleep(BACKUP_TASK_INTERVAL)
        timeCount += BACKUP_TASK_INTERVAL
        if timeCount > BACKUP_TASK_TIMEOUT:
            logging.error('VDS Backup timeout.')
            break
    if task.info.state == vim.TaskInfo.State.success:
        timeCount += BACKUP_TASK_INTERVAL
        logging.info("Successfully get VDS backup config objects.")
        return task.info.result
    logging.error("Failed to get VDS backup config objects.")
    return None

@logDeco.logFunction
def _isExistedPortGroup(portgroupConfig, portGroupList):
    """
    Description: check whether the portgroup is removed from the distributed switch
    :param portgroupConfig: portgroupConfig object, which is constructed from the backup file(dict)
                key, the key of the portgroupConfig object(String)
                name, the name of the portgroupConfig object(String)
    :param portGroupList: a list of portgroup object which is existed in the current distributed switch
    :return: if not removed return True, otherwise return False
    """
    for portGroup in portGroupList:
        if portgroupConfig['key'] == portGroup.key:
            return True
    return False

@logDeco.logFunction
def _restoreVDSBackupByType(dvsManager, backupConfigList, importType):
    """
    Description: restore the vdsBackup according to the backupConfigList and importType
    :param dvsManager: the distribute switch manager
    :param backupConfigList: backupConfigList is constructed from backup file(List)
    :param importType: 'applyToEntitySpecified' or 'createEntityWithOriginalIdentifier'
    :return: return taskResult if succeed, otherwise return None
    """
    vdsBackupConfigList = []
    for config in backupConfigList:
        vdsBackupConfig = vim.dvs.EntityBackup.Config()
        vdsBackupConfig.entityType = config['entityType']
        vdsBackupConfig.key = config['key']
        vdsBackupConfig.name = config['name']
        vdsBackupConfig.configBlob = config['configBlob']
        if importType == 'createEntityWithOriginalIdentifier':
            vdsBackupConfig.container = config['container']
        vdsBackupConfigList.append(vdsBackupConfig)
    task = dvsManager.DVSManagerImportEntity_Task(vdsBackupConfigList, importType)
    timeCount = 0
    while task.info.state == vim.TaskInfo.State.running:
        logging.debug('VDS backup restore is running, wait {0} more seconds.'.format(BACKUP_TASK_INTERVAL))
        time.sleep(BACKUP_TASK_INTERVAL)
        timeCount += BACKUP_TASK_INTERVAL
        if timeCount > BACKUP_TASK_TIMEOUT:
            logging.error('VDS backup restore timeout.')
            break
    if task.info.state == vim.TaskInfo.State.success:
        timeCount += BACKUP_TASK_INTERVAL
        return task.info.result
    return None

@logDeco.logFunction
def restoreVDSBackupConfig(serviceInstance, backupConfigList, vdsName):
    """
    Description: restore the vds backup
    :param serviceInstance: the connection of the vCenter
    :param backupConfigList: array of vdsBackupConfig object,
            'entityType', the entityType of the entity
            'key', the uuid of the DistributedVirtualSwitch or the id of the DistributedVirtualPortgroup
            'name', the name of the entity
            'configBlob', the configBlob of the entity
    :return: if succeed return the result, otherwise return none
    """
    dSwitch = getVDSByName(serviceInstance, vdsName)
    portGroupList = dSwitch.portgroup
    dvsManager = getDvsManager(serviceInstance)
    existedBackupConfigList = []
    notExistedBackupConfigList = []
    for config in backupConfigList:
        if config['entityType'] == 'distributedVirtualSwitch':
            existedBackupConfigList.append(config)
            continue
        if _isExistedPortGroup(config, portGroupList):
            existedBackupConfigList.append(config)
        else:
            config['container'] = dSwitch
            notExistedBackupConfigList.append(config)

    taskResult = _restoreVDSBackupByType(dvsManager, existedBackupConfigList, 'applyToEntitySpecified')
    if len(notExistedBackupConfigList) > 0 and taskResult:
        taskResult = _restoreVDSBackupByType(dvsManager, notExistedBackupConfigList, 'createEntityWithOriginalIdentifier')
    return taskResult

@logDeco.logFunction
def getEsxiHostObjectByName(serviceInstance, esxiHostName):
    """
    Description: Get Esxi host object by its name
    :param serviceInstance: service instance (get from connectTovCenter()) [OBJECT]
    :param esxiHostName: ESXI host name [STRING]
    :return: ESXI host object [OBJECT]
    """
    try:
        content = serviceInstance.RetrieveContent()
        esxiHostObj = getVSphereObj(content, [vim.HostSystem], esxiHostName)
        if not esxiHostObj:
            logging.warn('Found no host object for %s ' % esxiHostName)
            return None
        return esxiHostObj
    except Exception as e:
        logging.exception('Error occurred when getting host id for{0}, {1}'.format(esxiHostName, e.message))
        raise
        
@logDeco.logFunction
def getVDSByName(serviceInstance, vdsName):
    """
    Description: Get distributed switch by its name
    :param serviceInstance: service instance (get from connectTovCenter()) [OBJECT]
    :param vdsName: distributed switch name [STRING]
    :return: distributed switch [OBJECT]
    """
    try:
        content = serviceInstance.RetrieveContent()
        vdsObj = getVSphereObj(content, [vim.dvs.VmwareDistributedVirtualSwitch], vdsName)
        if not vdsObj:
            logging.warn('Found no vds object for %s ' % vdsName)
            return None
        return vdsObj
    except Exception as e:
        logging.exception('Error occurred when getting vds for{0}, {1}'.format(vdsName, e.message))
        raise

@logDeco.logFunction
def getVDSPortGroupByName(DVSwitch, portgroupName):
    """
    Description: Get distributed port group of a distributed switch
    :param DVSwitch: distributed switch [OBJECT]
    :param portgroupName: distributed port group name [STRING]
    :return: distributed port group [OBJECT]
    """
    try:
        portgroups = DVSwitch.portgroup
        pgs = filter(lambda x: x.name == portgroupName, portgroups)
        if len(pgs) > 0:
            return pgs[0]
        else:
            logging.warn('Found no port group with name %s' % portgroupName)
            return None
    except Exception as e:
        logging.exception('Error occurred when getting port group for{0}, {1}'.format(DVSwitch.name, e.message))
        raise


@logDeco.logFunction
def get_vswitch_obj(service_instance, vswitch_name):
    """
    Description: Get vswitch by its name
    :param service_instance: service instance of Esxi host [OBJECT]
    :param vswitch_name: vswitch name [STRING]
    :return: vswitch [OBJECT]
    """
    vswitch_obj = None
    try:
        content = service_instance.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder,
                                                            [vim.HostSystem], True)
        for host in container.view:
           for vswitch in host.config.network.vswitch:
               if vswitch.name == vswitch_name:
                   logging.info('Found vSwitch {0}'.format(vswitch_name))
                   vswitch_obj = vswitch

        if not vswitch_obj:
            logging.error('Found no vSwitch with name {0}'.format(vswitch_name))

        return vswitch_obj
    except Exception as err:
        logging.exception("Error occurred while finding vSwitch, error: %s",
                          str(err), exc_info=True)
        raise


@logDeco.logFunction
def find_vswitch_portgroup_by_name(vswitch_obj, port_group_name):
    """
    Description: Get port group of a vswitch
    :param vswitch_obj: vswitch [OBJECT]
    :param port_group_name:  port group name [STRING]
    :return: port group [OBJECT]
    """
    port_group_obj = None
    for portgroup in vswitch_obj.portgroup:
        pg_name = portgroup.split('key-vim.host.PortGroup-')[1]
        if pg_name == port_group_name:
            logging.info('Found port group with name %s' % port_group_name)
            port_group_obj = portgroup

    if not port_group_obj:
        logging.warn('Found no port group with name %s' % port_group_name)
    return port_group_obj


@logDeco.logFunction
def destroyVDSPortGroupByName(portGroupName, DVSwitch):
    """
    Description: Destroy distributed switch port group Id by its name
    :param content: get from connectTovCenter() [OBJECT]
    :param portGroupName: port group name [STRING]
    :param dvSwitchName: distributed virtual switch name [STRING]
    :return: task Id [STRING]
    """
    try:
        portGroupObj = getVDSPortGroupByName(DVSwitch, portGroupName)
        if not portGroupObj:
            logging.warn('PortGroup {0} object not found'.format(
            portGroupName))
            return None
        if portGroupObj.config.distributedVirtualSwitch == DVSwitch:
            return portGroupObj.Destroy_Task()
        else:
            logging.warn('PortGroup {0} does not belong to dvSwitch {1}'.format(
            portGroupName, DVSwitch.name))
            return None
    except Exception as e:
        logging.exception('Error occurred when destroying port group {0}, {1}'.format(
            portGroupName, e.message))
        raise

@logDeco.logFunction
def getHostObjsByCluster(serviceInstance, clusterName):
    """
    Description: Get ESXi host object list from Cluster
    :param serviceInstance: service instance (get from connectTovCenter()) [OBJECT]
    :param clusterName: cluster name [STRING]
    :return: Host Obj List [LIST]
    """
    try:
        hostList = []
        content = serviceInstance.RetrieveContent()
        clusterObj = getVSphereObj(content, [vim.ClusterComputeResource], clusterName)
        if not clusterObj:
            logging.info('Found no Cluster object for %s ' % clusterName)
            return None
        for hostObj in clusterObj.host:
            logging.info('Found ESXi host %s' % hostObj)
            hostList.append(hostObj)
        return hostList
    except Exception as e:
        logging.exception('Error occurred when getting hosts from cluster {0}, {1}'.format(clusterName, e.message))
        raise


@logDeco.logFunction
def rollingUninstallVIB(vCenterDict, clusterName, vibName, enterMaintenanceMode=True):
    """
    Uninstall VIB from each esxi hosts
    :param vCenterDict: dictionary containing vCenter information such as host, user
                        and password  [Dict]
    :param clusterName: vCenter cluster name [String]
    :param vibName: Name of VIB to be removed from each esxi host that belongs to A cluster[String]
    :param enterMaintenanceMode: True if host needs to be put in a maintenance mode before
                    uninstalling VIB [Boolean]
    :return: host uninstall status [Dict]
    """

    service_instance = connectToVcenter(vCenterDict['host'],
                                                    vCenterDict['user'],
                                                    vCenterDict["password"])
    atexit.register(connect.Disconnect, service_instance)

    hostObjects = getHostObjectsByCluster(service_instance, clusterName)
    result = {'succeeded': [], 'failed': [], 'skipped': [], 'status': True}
    for hostObject in hostObjects:
        try:
            if checkVIBInstalled(hostObject, vibName):
                exitMaintenanceMode = False
                msg = None
                failed = False
                if enterMaintenanceMode and not hostObject.runtime.inMaintenanceMode:
                    logging.info('Putting host: %s in maintenance mode', hostObject.name)

                    if not hostEnterMaintenanceMode(hostObject):
                        msg = "Failed to enter maintenance mode"
                        logging.info("%s: %s", hostObject.name, msg)
                        result['skipped'].append("%s: %s" % (hostObject.name, msg))
                        continue
                    exitMaintenanceMode = True
                try:
                    logging.info('Uninstalling VIB %s from host %s', vibName, hostObject.name)
                    uninstallVIB(hostObject, vibName)
                except Exception as ex:
                    msg = 'Failed to uninstall VIB %s Exception: %s' %\
                             (vibName, str(ex))
                    logging.exception("%s: %s", hostObject.name, msg, exc_info=True)
                    failed = True

                if exitMaintenanceMode:
                    logging.info('Exiting maintenance mode for host: %s', hostObject.name)
                    if not hostExitMaintenanceMode(hostObject):
                        msg = "Failed to exit maintenance mode"
                        logging.error('%s: %s', hostObject.name, msg)
                        failed = True

                if failed:
                    result['failed'].append("%s: %s" % (hostObject.name, msg))
                    result['status'] = False
                else:
                    result['succeeded'].append("%s: successfully uninstalled VIB %s" %
                                               (hostObject.name, vibName))
            else:
                logging.info('VIB %s is not installed on host %s', vibName, hostObject.name)
                result['skipped'].append('%s: VIB %s was not installed ' %
                                         (hostObject.name, vibName,))
        except Exception as ex:
            logging.exception("%s: %s", hostObject.name, str(ex), exc_info=True)
            result['failed'].append('%s: %s ' %  (hostObject.name, str(ex)))
            result['status'] = False

    return result


@logDeco.logFunction
def checkVIBInstalled(host, vibName):
    """
    Checks if a specified VIB is installed on a esxi host
    :param host: esxi Host object [vim.host]
    :param vibName: name of VIB to check [String]
    :return: True if VIB is installed on a host; otherwise False
    """
    logging.info("Scannning esxi host %s for vib %s", host.name, vibName)
    patchManager = host.configManager.patchManager
    task = patchManager.ScanHostPatchV2_Task()
    waitForTask(task)
    root = ET.fromstring(task.info.result.xmlResult)
    if root.findall("./vib-scan-data[name='{}']".format(vibName)):
        return True
    return False

def checkVIBInstalledVersion(host, vibName, vibVersion):
    """
    Checks if a specified VIB is installed on a esxi host
    :param host: esxi Host object [vim.host]
    :param vibName: name of VIB to check [String]
    :param vibVersion: version of VIB to check (String)
    :return: True if VIB of specific version is installed on a host;
    :        False if a different version is installed
    :        None if VIB is not installed  
    """
    logging.info("Scannning esxi host %s for vib %s", host.name, vibName)
    patchManager = host.configManager.patchManager
    task = patchManager.ScanHostPatchV2_Task()
    waitForTask(task)
    root = ET.fromstring(task.info.result.xmlResult)
    vibInfo = root.findall("./vib-scan-data[name='{}']".format(vibName))
    if vibInfo:
        version = vibInfo[0].findall('version')
        if version and vibVersion in version[0].text:
            return True
        else:
            return False
    return None


@logDeco.logFunction
def getVIBInstalledVersion(host, vibName):
    """
    get the VIB version specific VIB installed on a esxi host
    :param host: esxi Host object [vim.host]
    :param vibName: name of VIB to check [String]
    :return: True if VIB is installed on a host; otherwise False
    """
    version_dict = {'status': False, 'version': None, 'message': " "}
    try:
        logging.info("Scannning esxi host %s for vib %s", host.name, vibName)
        patchManager = host.configManager.patchManager
        task = patchManager.ScanHostPatchV2_Task()
        waitForTask(task)
        root = ET.fromstring(task.info.result.xmlResult)

        vibs = root.findall("./vib-scan-data[name='{}']".format(vibName))
        logging.info ("got the vib %s" %vibs)
        if vibs:
            for i in vibs:
                version_dict['version'] = i.find('version').text
                version_dict['status'] = True
                logging.info("VIB version for EXSI Host %s is %s"%(host.name,version_dict['version']))
        else:
            logging.info("Failed to get the VIB version on host %s"%str(host.name))
            version_dict['status'] = False
        return version_dict
    except RuntimeError as e:
        logging.info("Run time exception occured while scan on %s" %host.name)
        version_dict['status'] = False
        version_dict['message'] = e.message
    return version_dict


@logDeco.logFunction
def uninstallVIB(host, vibName):
    """
    Uninstalls the VIB from the specified esxi host
    :param host: esxi host [vim.host]
    :param vibName: name of VIB to uninstall [String]
    :return: True if uninstall is success;
    throws Exception on failure
    """
    patchManager = host.configManager.patchManager
    task = patchManager.UninstallHostPatch_Task(vibName)
    waitForTask(task)
    return True

@logDeco.logFunction
def getDRSVmBehavior (serviceInstance, clusterName, behavior):
    """
    Description: Get ESXi host list from Cluster
    :param serviceInstance: service instance (get from connectTovCenter()) [OBJECT]
    :param clusterName: cluster name [STRING]
    :return: Host FQDN/IP List [LIST]
    """
    try:
        content = serviceInstance.RetrieveContent()
        clusterObj = getVSphereObj(content, [vim.ClusterComputeResource], clusterName)
        if not clusterObj:
            logging.info('Found no Cluster object for %s ' % clusterName)
            return None
        return clusterObj.configuration.drsConfig;
    except Exception as e:
        logging.exception('Error set DRS vm Behavior cluster {0}, {1}'.format(clusterName, e.message))
        raise

@logDeco.logFunction
def setDRSVmBehavior (serviceInstance, clusterName, behavior):
    """
    Description: Get ESXi host list from Cluster
    :param serviceInstance: service instance (get from connectTovCenter()) [OBJECT]
    :param clusterName: cluster name [STRING]
    :return: Host FQDN/IP List [LIST]
    """
    try:
        content = serviceInstance.RetrieveContent()
        clusterObj = getVSphereObj(content, [vim.ClusterComputeResource], clusterName)
        if not clusterObj:
            logging.info('Found no Cluster object for %s ' % clusterName)
            return None
        drs_config=configure_drs(clusterObj.configuration.drsConfig,behavior)
        cluster_config_spec = vim.cluster.ConfigSpec()
        cluster_config_spec.drsConfig = drs_config
        task = clusterObj.Reconfigure(cluster_config_spec, True)
        waitForTask(task)
    except Exception as e:
        logging.exception('Error set DRS vm Behavior cluster {0}, {1}'.format(clusterName, e.message))
        raise


def configure_drs(drsConfig, behavior):
    """
    Description: configure DRS
    :param drsConfig: DRS
    :param behavior: behavior
    """
    vmbehavior= vim.cluster.DrsConfigInfo.DrsBehavior.fullyAutomated
    if behavior == "manual":
        vmbehavior =vim.cluster.DrsConfigInfo.DrsBehavior.manual
    if behavior == "fullyAutomated":
        vmbehavior =vim.cluster.DrsConfigInfo.DrsBehavior.fullyAutomated
    if behavior == "partiallyAutomated":
        vmbehavior = vim.cluster.DrsConfigInfo.DrsBehavior.partiallyAutomated

    # Set to partially automated
    drsConfig.defaultVmBehavior = vmbehavior
    return drsConfig