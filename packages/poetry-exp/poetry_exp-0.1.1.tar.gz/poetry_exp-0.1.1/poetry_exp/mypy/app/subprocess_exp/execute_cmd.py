"""
Passing shell=True:
              - Force to follow the semantics of shell in which it is executing
              - Spawn an intermediate shell to execute
              - Has security leaks
              -


Popen.communicate:
           - communicate() method returns a tuple (stdoutdata, stderrdata).
           - interacts with process: Send data to stdin.
           - Read data from stdout and stderr, until end-of-file is reached.
           - Wait for process to terminate.
The optional input argument should be a string to be sent to the
child process, or None, if no data should be sent to the child.

Basically, when you use communicate() it means that you want to
execute the command


It is safe to use stdout=PIPE and wait() together iff you read from the pipe.
communicate() does the reading and calls wait() for you
about the memory: if the output can be unlimited then you should not use .communicate()
                  that accumulates all output in memory.


For big output, we can give file
with open(my_large_output_path, 'w') as fo:
    with open(my_large_error_path, 'w') as fe:
        myProcess = Popen(myCmd, shell=True, stdout=fo, stderr=fe)
"""

from subprocess import Popen, PIPE


def execute_cmd(cmd, timeout=10):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    rc = p.wait() # will wait for the process to finish and return the exit code
    print rc
    if rc == 0:
        for line in p.stdout:
            print line
    else:
        for line in p.stderr:
            print line


def execute_cmd2(cmd, timeout=None):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    out, err = p.communicate()
    print p.returncode
    if p.returncode == 0:
        print out
    else:
        print err


def execute_cmd_with_shell(cmd, timeout=None):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    rc = p.wait() # This will wait for the process to finish
    if rc == 0:
        for line in p.stdout:
            print line
    else:
        for line in p.stderr:
            print line


if __name__ == '__main__':

    #Windows command, without shell=True
    execute_cmd('ping -n 1 localhost')
    execute_cmd('ipconfig')
    #execute_cmd2('ipconfig')  # or  execute_cmd2(['ipconfig'])
    execute_cmd2('python python_script.py')  #or execute_cmd2(['python', 'python_script.py'])
    #execute_cmd2('myshellscript.sh')

    #execute_cmd('date /T')
    #execute_cmd('ping localhost')
    #execute_cmd('ping -c 2 localhost')

    #execute_cmd('ipconfig2')  #without shell=True
    """
    Traceback (most recent call last):
    File "C:/Users/mohama30/Documents/EMC/repository/personal/cb-python/cb-python/python-demo/python-program/subprocess/program/execute_cmd.py", line 35, in <module>
    execute_cmd('ipconfig2')
  File "C:/Users/mohama30/Documents/EMC/repository/personal/cb-python/cb-python/python-demo/python-program/subprocess/program/execute_cmd.py", line 14, in execute_cmd
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
  File "C:\Python27\lib\subprocess.py", line 390, in __init__
    errread, errwrite)
  File "C:\Python27\lib\subprocess.py", line 640, in _execute_child
    startupinfo)
  WindowsError: [Error 2] The system cannot find the file specified
    """


    #execute_cmd_with_shell('ipconfig2')  # With shell=True
    """
    'ipconfig2' is not recognized as an internal or external command,
     operable program or batch file.
    """
