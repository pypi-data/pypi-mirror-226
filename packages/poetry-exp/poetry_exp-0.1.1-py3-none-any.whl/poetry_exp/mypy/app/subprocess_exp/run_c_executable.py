from subprocess import Popen, PIPE, TimeoutExpired

C_EXECUTABLE_PATH = '/home/aafak/run_c_from_py/test1'


def run_cmd(cmd, timeout=10):
    print(f'Executing command: {cmd}')
    try:
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate(timeout=timeout)
        rc = p.returncode
        print(f'rc: {rc}')
        print(f'Out: {out}, err: {err}')
    except TimeoutExpired as te:
        print(f'Timeout exception occurred, could not execute command :{cmd} in given time: {timeout}')
        print(f'Out: {p.stdout.read()}, err: {p.stderr.read()}') # # Will again wait to complete, so no use of it
        raise te


def run_cmd2(cmd, timeout=10):
    print(f'Executing command: {cmd}')
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    try:
        out, err = p.communicate(timeout=timeout)
        rc = p.returncode
        print(f'rc: {rc}')
        print(f'Out: {out}, err: {err}')
    except TimeoutExpired as te:
        print(f'Timeout exception occurred, could not execute command :{cmd} in given time: {timeout}')
        out, err = p.communicate(timeout=timeout)  # Will again wait to complete, so no use of it
        rc = p.returncode
        print(f'rc: {rc}')
        print(f'Out: {out}, err: {err}')
        if rc != 0:
            raise te


def run_cmd3(cmd, timeout=2):
    print(f'Executing command: {cmd}')
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    timeout_total_retry = 3
    timeout_retry_count = 0
    timeout_error = False
    while timeout_retry_count < timeout_total_retry:
        try:
            out, err = p.communicate(timeout=timeout)
            rc = p.returncode
            print(f'rc: {rc}')
            print(f'Out: {out}, err: {err}')
            timeout_error = False
            break
        except TimeoutExpired as te:
            print(f'Timeout exception occurred, could not execute command :'
                  f'{cmd} in given time: {timeout}, waiting for {timeout}'
                  f' sec to complete the process')
            timeout_retry_count += 1
            timeout_error = True

    if timeout_error:
        print('killing the process')
        p.kill()
        raise Exception(f'Failed to execute command :{cmd} due to timeout')


# https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate
"""
Popen.communicate(input=None, timeout=None)
Interact with process: Send data to stdin. Read data from stdout and stderr,
until end-of-file is reached. Wait for process to terminate and set the returncode attribute.
The optional input argument should be data to be sent to the child process, or None,
if no data should be sent to the child. If streams were opened in text mode, input must be a string. 
Otherwise, it must be bytes.

communicate() returns a tuple (stdout_data, stderr_data). The data will be strings if streams were opened
in text mode; otherwise, bytes.

Note that if you want to send data to the process’s stdin, you need to create the Popen
object with stdin=PIPE. Similarly, to get anything other than None in the result tuple,
 you need to give stdout=PIPE and/or stderr=PIPE too.

If the process does not terminate after timeout seconds, a TimeoutExpired exception will be raised.
Catching this exception and retrying communication will not lose any output.

The child process is not killed if the timeout expires, so in order to cleanup properly
a well-behaved application should kill the child process and finish communication:
"""
def run_cmd4(cmd, timeout=2):
    print(f'Executing command: {cmd}')
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    try:
        out, err = p.communicate(timeout=timeout)
        rc = p.returncode
        print(f'rc: {rc}')
        print(f'Out: {out}, err: {err}')
    except TimeoutExpired as te:
        print(f'Timeout exception occurred, could not execute command :{cmd} in given time: {timeout}')
        p.kill()
        out, err = p.communicate() # now it will not stuck, since we kill the process
        rc = p.returncode
        print(f'rc: {rc}')
        print(f'Out: {out}, err: {err}')


if __name__ == '__main__':
    run_cmd4(C_EXECUTABLE_PATH)


"""
aafak@aafak-virtual-machine:~/run_c_from_py$ pwd
/home/aafak/run_c_from_py
aafak@aafak-virtual-machine:~/run_c_from_py$ cat test1.c
#include <stdio.h>
int main() {
   // printf() displays the string inside quotation
   printf("Hello, World!");
   return 0;
}
aafak@aafak-virtual-machine:~/run_c_from_py$

aafak@aafak-virtual-machine:~/run_c_from_py$ gcc test1.c -o test1
aafak@aafak-virtual-machine:~/run_c_from_py$ ls
run_c_executable.py  test1  test1.c
aafak@aafak-virtual-machine:~/run_c_from_py$ chmod +x test1
aafak@aafak-virtual-machine:~/run_c_from_py$ ./test1
Hello, World!aafak@aafak-virtual-machine:~/run_c_from_py$

aafak@aafak-virtual-machine:~/run_c_from_py$ python3 run_c_executable.py
Executing command: /home/aafak/run_c_from_py/test1
rc: 0
Out: b'Hello, World!, sleeping...\ni:0\ni:1\ni:2\ni:3\ni:4\ni:5\ni:6\ni:7\ni:8\ni:9\ni:10\ni:11\ni:12\ni:13\ni:14\ni:15\ni:16\ni:17\ni:18\ni:19\n\nExecuted successfully\n', err: b''



CHange the timeout value to 10 and then run
aafak@aafak-virtual-machine:~/run_c_from_py$ python3 run_c_executable.py
Executing command: /home/aafak/run_c_from_py/test1
Timeout exception occurred, could not execute command :/home/aafak/run_c_from_py/test1 in given time: 10
Traceback (most recent call last):
  File "run_c_executable.py", line 19, in <module>
    run_cmd(C_EXECUTABLE_PATH)
  File "run_c_executable.py", line 16, in run_cmd
    raise te
  File "run_c_executable.py", line 10, in run_cmd
    out, err = p.communicate(timeout=timeout)
  File "/usr/lib/python3.8/subprocess.py", line 1028, in communicate
    stdout, stderr = self._communicate(input, endtime, timeout)
  File "/usr/lib/python3.8/subprocess.py", line 1869, in _communicate
    self._check_timeout(endtime, orig_timeout, stdout, stderr)
  File "/usr/lib/python3.8/subprocess.py", line 1072, in _check_timeout
    raise TimeoutExpired(
subprocess.TimeoutExpired: Command '/home/aafak/run_c_from_py/test1' timed out after 10 seconds
aafak@aafak-virtual-machine:~/run_c_from_py$



"""