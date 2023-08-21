from functools import wraps
import asyncio
from datetime import datetime
import time
import requests

loop = asyncio.get_event_loop()


async def get_web_page(url):
    return await requests.get(url)


class RequestIterator:
    def __init__(self, urls, task_name):
        self.urls = urls
        self.task_name = task_name

    def __await__(self):
        print ('Calling await...{0}'.format(self.task_name))
        for url in self.urls:
            print('[{0}]: Executing request: {1}'.format(self.task_name, url))
            response = get_web_page(url)
            print('[{0}]: response: {1} for url: {2}'.format(self.task_name, response, url))
        return self


async def async_task(urls, task_name):
   print('Executing task: {0}'.format(task_name))
   await RequestIterator(urls, task_name) #  asyncio.sleep(1)
   print('Finished task: {0}'.format(task_name))


def execute_async_task():
    print("Time: {0}, Async Task Started".format(datetime.now()))
    tasks = []
    urls = [
        'http://localhost:5000/home',
        'http://localhost:5000/index',
    ]
    for i in range(5):
        task = asyncio.ensure_future(async_task(urls, "Task"+str(i)))
        tasks.append(task)

    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
    print("Time: {0}, Closing the loop".format(datetime.now()))
    loop.close()
    print("Time: {0}, Async Task End".format(datetime.now()))


if __name__ == '__main__':
    # execute_sync_task()  # takes 5 min
    execute_async_task()  # takes only less than 20 sec
    #loop.run_until_complete(async_task("trask1"))

