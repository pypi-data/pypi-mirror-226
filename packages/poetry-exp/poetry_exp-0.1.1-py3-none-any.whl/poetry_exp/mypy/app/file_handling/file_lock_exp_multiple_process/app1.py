from app.file_handling.file_lock_exp_multiple_process import lock_utils

APP = 'app1'
if __name__ == '__main__':

    lock_utils.write_file_with_retry(txt=f'{APP} data')


"""
C:\Python3\python.exe "C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/app/file_handling/file_lock_exp_multiple_process/app1.py"
[6920] Lock acquired for writing to file...
[6920] Closed file
"""