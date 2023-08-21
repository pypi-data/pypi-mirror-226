from filelock import FileLock
import time
import os
from filelock import Timeout


PID = os.getpid()


def write_file_with_retry(file_name="a.txt", txt='', lock_timeout=5, max_retry=5):
    count = 0
    while count < max_retry:
        try:
           write_file(file_name=file_name, txt=txt, lock_timeout=lock_timeout)
           break
        except Timeout as e:
            count += 1
            print(f'[{PID}] Could not acquired the lock on file, error:{e}, retrying...{count}/{max_retry}')
    else:
        print(f'[{PID}] Could not write on file')


def write_file(file_name="a.txt", txt='', lock_timeout=10):
    with FileLock(str(file_name) + ".lock", timeout=lock_timeout):
        print(f"[{PID}] Lock acquired for writing to file...")
        time.sleep(20)
        f = open(file_name, "a")
        f.write(f"Wrote by process({PID}): {txt}\n")
        f.close()
        print(f"[{PID}] Closed file")


