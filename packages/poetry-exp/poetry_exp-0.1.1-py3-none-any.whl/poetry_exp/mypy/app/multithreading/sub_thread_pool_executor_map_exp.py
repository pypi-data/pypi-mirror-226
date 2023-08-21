import concurrent
from concurrent.futures import ThreadPoolExecutor
from os import getpid
import time


def worker(procnum):
    #print (greeting)
    print ('I am number %d in process %d' % (procnum, getpid()))
    return getpid()


class jobComponent:
    def __init__(self, job_id, job_status):
        self.job_id = job_id
        self.job_status = job_status


def worker2(data):
    try:
        print(f'Processing data: {data}')
        time.sleep(5)
        if data['id'] == 2:
            raise ValueError("Invalid value")
        return {'result': {'status': True, "data": data}}
    except Exception as e:
        return {'result': {'status': False, "data": data, 'error': str(e)}}


def process_sub_tasks(task_id, task_name, job_comp):
    print(f'[{getpid()}]: Processing sub tasks for {task_id}, Name: {task_name}')
    sub_tasks = [{"id": "sub_task-"+str(i), 'name': "sub_task-"+str(i)} for i in range(5)]
    thread_pools = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for task in sub_tasks:
            thread_pools.append(executor.submit(process_task, task['id'], task['name']))

    concurrent.futures.wait(thread_pools)

    job_comp.job_status = "Ok"


def process_task(task_id, task_name, job_comps):
    print(f'[{getpid()}]: Processing task: {task_id}, Name: {task_name}')
    for job_comp in job_comps:
        if 'sub_task' not in task_name:
            process_sub_tasks(task_id, task_name, job_comp)
            job_comp.job_status = 'Ok2'


def execute_task(tasks):
    thread_pools = []
    job_comps = [jobComponent(1, "Error"), jobComponent(2, "Error")]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for task in tasks:
            thread_pools.append(executor.submit(process_task, task['id'], task['name'], job_comps))

    concurrent.futures.wait(thread_pools)

    for job_comp in job_comps:
        print(job_comp.job_id, job_comp.job_status)


if __name__ == '__main__':
    t1 = time.time()
    tasks = [{"id": "task-"+str(i), 'name': "task-"+str(i)} for i in range(1)]

    execute_task(tasks)
    t2 = time.time()
    print(f'Time taken to process: {t2-t1} sec')

# 21.2 with 1 process
# 11.2 with 2 process
# 11.4 with 3 process
# 6.9 with 4 process
# In short , no of process will become a batch of task running parellely