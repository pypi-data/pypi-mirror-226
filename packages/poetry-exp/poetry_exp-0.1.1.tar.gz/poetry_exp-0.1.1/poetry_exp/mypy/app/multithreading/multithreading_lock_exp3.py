from threading import Thread, Lock
import time
import os

l = Lock()
lock_dict = dict()

def is_locked(lock):
    locked = lock.acquire()
    if locked == False:
        #print('lock: {0} is locked'.format(lock))
        return True
    else:
        #print('lock: {0} is not locked'.format(lock))
        lock.release()
        return False

# Thread synchronization
def f(l, i):
    # Lock dict will be accesible and updateble from all the thread
    print(f'Thread: {i}, acquiring lock..., lock dict: {lock_dict}, pid: {os.getpid()}')
    lock_dict[i] = l
    lock_acquire_result = l.acquire(timeout=100)
    print(f'Thread: {i}, acquired lock, result: {lock_acquire_result},,'
          f' lock dict: {lock_dict}, pid: {os.getpid()}')
    print(f'Thread: {i}, starts execution....., pid: {os.getpid()}')
    # Critical section of the code
    for k in range(5):
        print(f'Thread:{i}, data: {k} ')
        time.sleep(5)
    print(f'Thread: {i}, execution completed., pid: {os.getpid()}')

    if is_locked(l):
        print(f'Thread: {i}, releasing lock., pid: {os.getpid()}')
        l.release()

if __name__ == '__main__':
    jobs = []
    for num in range(10):
        p = Thread(target=f, args=(l, num))
        # p.start()
        jobs.append(p)
    for j in jobs:
        j.start()

    for j in jobs:
        j.join()


"""
C:\Python3\python.exe "C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/multithreading/multiprocessing_lock_exp.py"
process:1, data: 0 
process:1, data: 1 
process:1, data: 2 
process:1, data: 3 
process:1, data: 4 
process:0, data: 0 
process:0, data: 1 
process:0, data: 2 
process:0, data: 3 
process:0, data: 4 
process:2, data: 0 
process:2, data: 1 
process:2, data: 2 
process:2, data: 3 
process:2, data: 4 
process:3, data: 0 
process:3, data: 1 
process:3, data: 2 
process:3, data: 3 
process:3, data: 4 
process:5, data: 0 
process:5, data: 1 
process:5, data: 2 
process:5, data: 3 
process:5, data: 4 
process:4, data: 0 
process:4, data: 1 
process:4, data: 2 
process:4, data: 3 
process:4, data: 4 
process:9, data: 0 
process:9, data: 1 
process:9, data: 2 
process:9, data: 3 
process:9, data: 4 
process:6, data: 0 
process:6, data: 1 
process:6, data: 2 
process:6, data: 3 
process:6, data: 4 
process:7, data: 0 
process:7, data: 1 
process:7, data: 2 
process:7, data: 3 
process:7, data: 4 
process:8, data: 0 
process:8, data: 1 
process:8, data: 2 
process:8, data: 3 
process:8, data: 4 

Process finished with exit code 0

"""