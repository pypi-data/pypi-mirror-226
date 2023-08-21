

import copy
import logging
import os
import sys
import tempfile
import time
from subprocess import Popen, PIPE, STDOUT

import psutil
from common.log import logDeco
from common.pyvmomiUtil import exeRemoteCommand
from conf.constants import OSType, POWERSHELL_PARAMS, DEFAULT_TIMEOUT_SECS, REMOTE_EXECUTION_PARAMS

@logDeco.logFunction
def executelocalPS(targetPS, params=None, inputType="cmd", executionPolicy="Unrestricted", timeout=None, **kwargs):
    """
    Description:
        This method is used to execute powershell script locally
    Parameters:
        targetPS        : target powershell script or commmand to execute (STRING)
        params          : Parameters to the script (LIST)
                          Note : Parameter values with spaces enclosed in single quote
        inputType       : Type of command file\cmd (STRING)
        executionPolicy : powershell execution policy (STRING)
        timeout       : [OPTIONAL]timeout in seconds (INT)
        dnLogParam    : [OPTIONAL]Parameters which should not be logged
    Returns: True and output
    Raises: If error in powershell execution, 'Error executing powershell script.'
            exception is raised
            If timed out 'Powershell process timed out.' exception is raised
    """
    try:
        logging.info("Executing powershell on local: %s", targetPS)
        if inputType == "file":
            targetPS = 'Set-ExecutionPolicy %s; Invoke-Expression ' \
                        '"& `"%s`" %s"' % (executionPolicy, targetPS, ' '.join(params))

        processArgs = getLocalProcessArgs(targetPS, executionPolicy)

        processObj = Popen(processArgs, stdin=PIPE,
                           stderr=STDOUT, stdout=PIPE, bufsize=1)

        # remove parameters which should not be logged
        password_val = None
        for key in kwargs.get('dnLogParam', []):
            if key in params:
                if key == "-OvfConfigValues":
                    #Stripping the password from -OvfConfigValues value
                    password_val = eval((params[params.index(key) + 1]))[0]
                params = params[:params.index(key)] + params[params.index(key) + 2:]


        logging.info("Parameters to the script: %s", ' '.join(params))
        if timeout:
            status = waitForPSExecution(processObj, timeout)
            if status == -1:
                message = 'Powershell process timed out.'
                logging.exception(message)
                raise Exception(message)
        stdOut = processObj.communicate()[0]
        checkErrorInPSOutput(stdOut)

        message = "Powershell %s executed successfully." % inputType
        logging.info(message)
        if password_val != None:
            stdOut=stdOut.replace(password_val,"*********")
        logging.info(stdOut)
        return True, stdOut
    except Exception as ex:
        message = "Local powershell execution failed"
        logging.exception(message)
        raise

def getLocalProcessArgs(targetPS, executionPolicy):
    """
    Description:
        Constructs the subprocess' list of arguments based on the system's platform
    :param targetPS: Powershell command to be executed
    :param executionPolicy: Subprocess' execution policy
    :return: List of arguments to the subprocess
    """

    # If platform is Linux, assume we're root instead of running with elevated permissions
    if "linux" in sys.platform:
        runAsScript = '-c'
        execStr = ' '.join(['{', targetPS, '}'])
        args = ["powershell", '-ExecutionPolicy', executionPolicy, runAsScript, execStr]
    else:
        runAsScript = POWERSHELL_PARAMS['runasadminscript']
        currentDir = os.path.dirname(os.path.realpath(__file__))
        runAsScript = os.path.join(currentDir, runAsScript)
        execStr = ' '.join([runAsScript, '{', targetPS, '}'])
        args = ["powershell", '-ExecutionPolicy', executionPolicy, execStr]
    return args

def killProcess(processID):
    """
    Description:
        This method is used to kill process and child processes
    Parameters:
        processID : process ID (INT)
    Returns:
    """
    parent = psutil.Process(processID)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()

def waitForPSExecution(processObj, timeout=DEFAULT_TIMEOUT_SECS):
    """
    Description:
        This method waits for subprocess to execute for specific seconds
    Parameters:
        processObj     : powershell subprocess object (OBJECT)
        timeout       : [OPTIONAL]timeout in seconds (INT)
    Returns: status of process execution
            0 - success
           -1 - timeout
    """
    waitRemainingSec = timeout

    while processObj.poll() is None and waitRemainingSec > 0:
        time.sleep(1)
        waitRemainingSec -= 1

    if waitRemainingSec <= 0:
        killProcess(processObj.pid)
        return -1
    return 0

@logDeco.logFunction
def checkErrorInPSOutput(output):
    """
    Description:
        This method is used to check error in output of powershell execution
    Parameters:
        output   : output of powershell script (STRING)
    Returns: None if no error in output
    Raises: If error in powershell output, 'Error executing powershell script.'
            exception is raised
    """
    if POWERSHELL_PARAMS['powershellerrorpattern'] in output:
        message = "Error executing powershell script."
        logging.exception(output)
        raise Exception(message)


@logDeco.logFunction
def executeremotePS(vCenterDict, vMDict, targetPS, params=None, inputType="cmd", timeout=None):
    """
    Description:
        This method is used to execute powershell on remote machine using pyvmomi library.
    Parameters:
        vCenterDict   : Dictionary containing vcenter details (DICT)
        vMDict        : Dictionary containing vm details (DICT)
        targetPS      : Target powershell script/command (STRING)
        params        : Parameters to the script (LIST)
        inputType     : script type cmd\file (STRING)
        timeout       : [OPTIONAL] The maximum time (in seconds) for which to
                                wait for the program to complete.(INT)
    Returns: True and output
    Raises: If error in powershell execution, 'Error executing powershell script.'
            exception is raised
    """
    try:
        if not params:
            params = []

        scriptDict = {}
        #remote OS type for powershell execution always WINDOWS
        powershellExec = {'ostype': OSType.WINDOWS}
        vMDict.update(powershellExec)
        #create a file if input is command
        if inputType == "cmd":
            with tempfile.NamedTemporaryFile(
                mode='w+b', delete=False,
                prefix=REMOTE_EXECUTION_PARAMS['orch_vm']['prefix'],
                suffix=''.join([REMOTE_EXECUTION_PARAMS['orch_vm']['suffix'], '.ps1']),
                dir=REMOTE_EXECUTION_PARAMS['orch_vm']['tmpdir']
            ) as tmpFile:
                tmpFile.write(targetPS)
                tmpFile.close()
                targetPS = tmpFile.name

        scriptDict['localScriptPath'] = targetPS
        scriptDict['remoteShellPath'] = POWERSHELL_PARAMS['executable']
        scriptDict['args'] = params
        if timeout:
            scriptDict['timeout'] = timeout

        #call the pyvmomiUtils helper function to execute remote command on guest VM
        status, localOutFile = exeRemoteCommand(vCenterDict, vMDict, scriptDict)
        #remove the temporary file created in case of command as input
        if inputType == "cmd":
            os.remove(targetPS)

        with open(localOutFile, "r+") as outFile:
            output = outFile.read()
            checkErrorInPSOutput(output)
            message = "Powershell %s executed successfully." % inputType
            logging.info(message)
            return True, output

    except:
        message = "Remote powershell execution failed: %s" % targetPS
        logging.exception(message)
        raise


@logDeco.logFunction
def validateexecutePSlocal(targetPS, params=None, inputType="cmd", executionPolicy="Unrestricted"):
    """
    Description:
        Execute and validate powershell execution on local machine
    Parameters:
        targetPS        : target powershell script or commmand to execute (STRING)
        params          : Parameters to the script (LIST)
        inputType       : Type of command file\cmd (STRING)
        executionPolicy : powershell execution policy (STRING)
    Returns: Status of validation True/False
    """
    try:
        status, output = executelocalPS(targetPS, params, inputType, executionPolicy)
        if not status:
            logging.critical('Validation for local Powershell execution failed.')
            return False

        logging.info('Validation for local Powershell successful.')
        return True
    except:
        logging.exception('Exception in local powershell validation.')
        raise


@logDeco.logFunction
def validateexecutePSremote(vCenterDict, vmDict, targetPS, params=None, inputType="cmd"):
    """
    Description:
        Execute and validate powershell execution on remote machine
    Parameters:
        vCenterDict   : Dictionary containing vcenter details (DICT)
        vMDict        : Dictionary containing vm details (DICT)
        targetPS      : Target powershell script/command (STRING)
        params        : Parameters to the script (LIST)
        inputType     : script type cmd\file (STRING)
    Returns: Status of validation True/False
    """
    try:
        status, output = executeremotePS(vCenterDict, vmDict,
                                         targetPS, params, inputType)
        if not status:
            logging.critical('Validation for remote Powershell execution failed.')
            return False
        logging.info('Validation for remote Powershell successful.')
        return True
    except:
        logging.exception('Exception in local powershell validation.')
        raise
