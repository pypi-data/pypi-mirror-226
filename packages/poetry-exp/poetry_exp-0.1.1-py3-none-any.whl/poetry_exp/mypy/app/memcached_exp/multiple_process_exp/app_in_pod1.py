import bmemcached
from datetime import datetime
import time
import json
import os
import random

memcache_client = bmemcached.Client(('127.0.0.1:11211',))

POD_NAME = "Pod1"


def create_bkp_lock(res_id):
    bkp_res_key = "__bkp__{0}".format(res_id)
    res_bkp_lock_key_added = memcache_client.add(
        bkp_res_key, json.dumps({'lockByPod': POD_NAME,
                                 'resourceId': res_id,
                                 'createdAt': str(datetime.now())}
                                )
    )
    if res_bkp_lock_key_added:
        print(f'[pid: {os.getpid()}] [{POD_NAME}] Acquired backup lock for resource:{res_id}')
    else:
        res_bkp_lock_info = memcache_client.get(bkp_res_key)
        print(f'[pid: {os.getpid()}] [{POD_NAME}] Error: Resource: {res_id} is already locked for backup creation,'
              f' res_bkp_lock_info: {res_bkp_lock_info}')
        raise Exception(f"Failed to acquired backup lock for resource: {res_id}")


def release_bkp_lock(res_id):
    bkp_res_key = "__bkp__{0}".format(res_id)
    memcache_client.delete(bkp_res_key)
    print(f'[pid: {os.getpid()}] [{POD_NAME}] Released backup lock for resource:{res_id}')


def create_bkp(res_id):
    bkp_lock_acquired = False
    try:
        create_bkp_lock(res_id)
        bkp_lock_acquired = True
        print(f'[pid: {os.getpid()}] [{POD_NAME}] Creating backup for resource: {res_id}...')
        for i in range(1, 16):
            print(f'[pid: {os.getpid()}] [{POD_NAME}] Creating backup... step: {i}/{15}')
            time.sleep(0.50)

        print(f'[pid: {os.getpid()}] [{POD_NAME}] Successfully created the backup for resource: {res_id}')
    except Exception as e:
        print(f'[pid: {os.getpid()}] [{POD_NAME}] Failed to create the backup for resource:{res_id}, error: {e}')
    finally:
        if bkp_lock_acquired:
            release_bkp_lock(res_id)


if __name__ == '__main__':

    res_ids = [1]
    while True:
        resource_id = "res-uuid-" + str(random.choice(res_ids))
        create_bkp(resource_id)
        print(f'Waiting...')
        time.sleep(10)