from multiprocessing import Process, Lock, Manager
import time
import os
import random

#GET_RESOURCE_LOCK = Lock()

# For getting/Creating the resource lock
#GET_RESOURCE_LOCK = Lock()
GET_RESOURCE_LOCK_TIMEOUT = 60  # 1min

def acquire_resource_lock(lock_dict, resource_id, timeout):
    lock = get_or_create_resource_lock(lock_dict,  resource_id)
    lock.acquire(timeout=timeout)
    print(f'........lockdict: {lock_dict}')


def release_resource_lock(lock_dict, resource_id):
    print(f'lock_dict: {lock_dict}')
    print(f'..............resource_id:: {resource_id}')
    if resource_id in lock_dict:
        lock = lock_dict[resource_id]
        if lock and is_locked(lock):
            print(f'Release Resource: {resource_id} lock')
            lock.release()


def get_or_create_resource_lock(lock_dict, resource_id):
    try:
        print(f'...Existing locks: {lock_dict}')
        #GET_RESOURCE_LOCK.acquire(timeout=GET_RESOURCE_LOCK_TIMEOUT)

        if resource_id in lock_dict:
            print('comes here.....')
            return lock_dict[resource_id]
        else:
            print(f'Lock not exist for resource: {resource_id},'
                     f' creating it')
            m = Manager()
            lock = m.Lock()
            lock_dict[resource_id] = lock
            return lock
    finally:
        #GET_RESOURCE_LOCK.release()
      pass



def is_locked(lock):
    locked = lock.acquire(block=False)
    if locked == False:
        #print('lock: {0} is locked'.format(lock))
        return True
    else:
        #print('lock: {0} is not locked'.format(lock))
        lock.release()
        return False


def refresh_resource(lock_dict):
    res_id = "res-" + str(random.randint(1, 2))
    print(f'Received refresh resource: {res_id} request')
    acquire_resource_lock(lock_dict, res_id, 100)
    print(f'Resource: {res_id} acquired lock')
    for k in range(5):
        print(f'Refreshing Resource:{res_id}, step: {k} ')
        time.sleep(1)
    release_resource_lock(lock_dict, res_id)


if __name__ == '__main__':
    jobs = []
    lock_dict = Manager().dict()

    for num in range(7):
        p = Process(target=refresh_resource, args=(lock_dict,))
        jobs.append(p)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

