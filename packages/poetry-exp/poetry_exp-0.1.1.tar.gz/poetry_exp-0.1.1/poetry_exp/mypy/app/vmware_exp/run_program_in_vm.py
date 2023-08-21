"""
Steps:
1. Connect to vcenter
2. Get the VM Object
3. Create Credential object
4. ensure guest tool running
5. upload script file to vm containing command to run
6. Create temp file in vm to store the command output
7. form args list to store the output in temp file
8. create program spec
9. Using ProcessManager object and call the StartProgramInGuest method, will return the process id
10. wait for program to exit- List Process in guest and check the exit code of process id
11. Download the outfile from VM
12. Parse the content of file and check the result
13. Delete the script and output file from guest
14. Disconnect to vcenter



si = connectToVcenter(vCenterConfDict['host'], vCenterConfDict['user'], vCenterConfDict['password'])
vm = getVMByName(si, vmConfDict['vmname'])
cred = vim.vm.guest.NamePasswordAuthentication(username=guestUsername, password=guestPassword)
ensureGuestToolsRunning(vm)
remoteScriptPath = uploadFileToVM(serviceInstance, virtualMachine, guestOSCredentials, localScriptPath, guestOSType, hostIP=hostIP)
remoteOutFilePath = _createTempFile(serviceInstance, virtualMachine, guestOSCredentials, guestOSType)
arglist = [remoteScriptPath, '>', remoteOutFilePath, '2>&1']
progSpec = vim.vm.guest.ProcessManager.ProgramSpec(programPath=remoteShellPath, arguments=' '.join(arglist))
pm = serviceInstance.content.guestOperationsManager.processManager
pid = pm.StartProgramInGuest(vm, cred, progSpec)
exit_staus = False
while exit_staus is False:
    remoteProcessInfo = pm.ListProcessesInGuest(virtualMachine, guestOSCredentials, [pid])[0]
    attrToCheck = 'exitCode'
    exit_staus = hasattr(remoteProcessInfo, attrToCheck) and getattr(remoteProcessInfo, attrToCheck) is not None

localOutFilePath = downloadFileFromVM(serviceInstance, virtualMachine, guestOSCredentials, remoteOutFilePath)

"""

from pyVmomi import vim
from pyVim import connect
import ssl
import logging
import requests
import os
import time
import tempfile


class OSType(object):
    LINUX, WINDOWS = range(2)

params = {
    'orch_vm': {


        'tmpdir': 'C:\\ehc',
        'prefix': 'EHCAutoPrefix',
        'suffix': 'EHCAutoSuffix',
        'encoding': 'utf-8'
    },
    'execution_vm': {
        OSType.LINUX: {
            'tmpdir': '/tmp',
            'prefix': 'EHCAutoPrefix',
            'suffix': 'EHCAutoSuffix',
        },
        OSType.WINDOWS: {
            'tmpdir': 'C:\\ehc',
            'prefix': "EHCAutoPrefix",
            'suffix': "EHCAutoSuffix",
        },
    },
}


def connectToVcenter(vCenterHost, username, password, portNum ):
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    sslcontext.verify_mode = ssl.CERT_NONE

    try:
        # Call to connect to given vCenterIP
        serviceInstance = connect.SmartConnect(host=vCenterHost, user=username,
                                               pwd=password, port=portNum,
                                               sslContext=sslcontext)
        logging.info("Connecting to : %s, with username: %s" % (vCenterHost, username))
        return serviceInstance
    except:
        message = "Failed to Connect to -{0} user-{1}".format(vCenterHost, username)
        logging.exception(message)
        raise


def getVMByName(serviceInstance, name):
    """
    Description: Find a virtual machine by it's name
    Parameters: serviceInstance: vCenter connection session (OBJECT)
                name: virtual machine name (STRING)
    Return: virtual machine Object (OBJECT)
    Raises: RuntimeError if the virtual machine cannot be found.
    """
    vm = None
    content = serviceInstance.RetrieveContent()
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vmObj in container.view:
        if vmObj.name == name:
            return vmObj


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

    # ensureGuestToolsRunning(virtualMachine)
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

    #ensureGuestToolsRunning(virtualMachine)
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


def _getFileExt(filename):
    """
    Description: Get extension of filename.
    Parameters: filename: The filename whose extension is needed. (STRING)
    Returns: The extension of filename (with the '.'), or '' if the file does not
             have an extension. (STRING)
    """
    return os.path.splitext(filename)[1]


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
    #_loggingVMAccess(guestOSCredentials, virtualMachine)
    #ensureGuestToolsRunning(virtualMachine)
    fm = serviceInstance.content.guestOperationsManager.fileManager
    fm.DeleteFileInGuest(virtualMachine, guestOSCredentials, remoteFilename)


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
