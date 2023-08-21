from functools import wraps
import asyncio
from datetime import datetime
import time
import requests

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

"""
    'https://www.python.org',
    'https://www.google.com',
"""

urls = [
    'http://localhost:5000/home',
    'http://localhost:5000/home',

    ]

def get_web_page(url):
    return requests.get(url)

def sync_task(task_name):
    for url in urls:
       print('Time: {0}, Executing task: {1}, Fetching web page: {2}'.format(datetime.now(), task_name, url))
       get_web_page(url)

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


async def stop_after(loop, when):
    await asyncio.sleep(when)
    print("Time: {0}, Stopping the loop".format(datetime.now()))
    loop.stop()


async def get_page(url):
    return requests.get(url)


class Counter:
    def __init__(self, low, high):
        self.current = low - 1
        self.high = high

    def __iter__(self):
        return self

    def __next__(self): # Python 2: def next(self)
        self.current += 1
        if self.current < self.high:
            return self.current
        raise StopIteration


class RequestIterator:
    def __init__(self, urls):
        self.urls = urls

    def __iter__(self):
        return self

    def __next__(self):
        if not self.urls:
            raise StopIteration
        else:
           url = self.urls.pop()
           print('Executing request: {0}'.format(url))
           response = requests.get(url)
           print('response: {0}'.format(dir(response)))
           #response.status_code = 200
           return response


class MyRequest:
    def __init__(self, urls):
        self.urls = urls

    def __await__(self):
        return RequestIterator(self.urls)


async def async_task(task_name):
   print('Executing task: {0}'.format(task_name))
   await MyRequest(urls)
   print('Finished task: {0}'.format(task_name))



def execute_async_task():
    print("Time: {0}, Async Task Started".format(datetime.now()))
    for i in range(5):
        # 30 Task, each task takes 10 sec, 30*10 = 300 sec  , 300/60 = 5 min,
        # but takes only less than 20 sec
        loop.create_task(async_task("Task"+str(i)))

    loop.create_task(stop_after(loop, 30))
    loop.run_forever()
    print("Time: {0}, Closing the loop".format(datetime.now()))
    loop.close()
    print("Time: {0}, Async Task End".format(datetime.now()))


"""  Less than 20 sec
Time: 2019-12-04 15:24:17.006643, Async Task Started
Time: 2019-12-04 15:24:32.010389, Stopping the loop
Time: 2019-12-04 15:24:32.010389, Closing the loop
Time: 2019-12-04 15:24:32.010389, Async Task End
"""






if __name__ == '__main__':
    # execute_sync_task()  # takes 5 min
    execute_async_task()  # takes only less than 20 sec
    #loop.run_until_complete(async_task("trask1"))

