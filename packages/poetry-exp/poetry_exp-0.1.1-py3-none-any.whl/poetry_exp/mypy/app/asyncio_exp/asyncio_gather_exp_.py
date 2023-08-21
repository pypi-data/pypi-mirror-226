from functools import wraps
import asyncio
from datetime import datetime
import time

loop = asyncio.get_event_loop()


def logit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print('Function: {0}, total time: {1}'.format(func.__name__, (t2-t1)))
        return result
    return wrapper


def sync_task(task_name):
    for i in range(11):
       print('Time: {0}, Executing task: {1}, progress: {2}%'.format(datetime.now(), task_name, i*10))
       time.sleep(1)

@logit
def execute_sync_task():
    print("Time: {0}, Sync Task Started".format(datetime.now()))
    for i in range(31):  # 30 Task, each task takes 10 sec, 30*10 = 300 sec  , 300/60 = 5 min
        sync_task("Task"+str(i))
    print("Time: {0}, Sync Task End".format(datetime.now()))

"""
Time: 2019-12-04 15:26:17.143026, Sync Task Started
Time: 2019-12-04 15:31:58.493714, Sync Task End
Function: execute_sync_task, total time: 341.350688457489
"""


async def async_task(task_name):
    for i in range(11):
       print('Time: {0}, Executing task: {1}, progress: {2}%'.format(datetime.now(), task_name, i*10))
       await asyncio.sleep(1)


def execute_async_task():
    print("Time: {0}, Async Task Started".format(datetime.now()))
    tasks = []
    for i in range(31):  # 30 Task, each task takes 10 sec, 30*10 = 300 sec  , 300/60 = 5 min, but takes only less than 20 sec
        task = asyncio.ensure_future(async_task("Task"+str(i)))
        tasks.append(task)

    loop.run_until_complete(asyncio.gather(*tasks))
    print("Time: {0}, Closing the loop".format(datetime.now()))
    loop.close()
    print("Time: {0}, Async Task End".format(datetime.now()))


"""  Less than 20 sec
Time: 2019-12-05 12:37:47.764713, Async Task Started
Time: 2019-12-05 12:37:58.782984, Closing the loop
Time: 2019-12-05 12:37:58.782984, Async Task End
"""

if __name__ == '__main__':
    # execute_sync_task()  # takes 5 min
    execute_async_task()  # takes only less than 15 sec

