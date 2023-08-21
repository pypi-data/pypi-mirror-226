from app.file_handling.file_lock_exp_multiple_process import lock_utils

APP = 'app2'
if __name__ == '__main__':
    lock_utils.write_file_with_retry(txt=f'{APP} data')


"""
C:\Python3\python.exe "C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/app/file_handling/file_lock_exp_multiple_process/app2.py"
[18028] Could not acquired the lock on file, error:The file lock 'a.txt.lock' could not be acquired., retrying...1/5
[18028] Could not acquired the lock on file, error:The file lock 'a.txt.lock' could not be acquired., retrying...2/5
[18028] Could not acquired the lock on file, error:The file lock 'a.txt.lock' could not be acquired., retrying...3/5
[18028] Lock acquired for writing to file...
[18028] Closed file
"""