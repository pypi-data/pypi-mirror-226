import asyncio
import threading
import time


async def task1():
    for i in range(3):
        await asyncio.sleep(1)
        print(f'Running i: {i}')
    print('Completed task1')
    return 1


async def call_task1():
   n = await task1()
   return n


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # futures = [call_task1()]

    response = loop.run_until_complete(asyncio.wait([call_task1()]))
    print(f"Result : {type(response)}")
    print(f'Result: {response.count(0)}')
    print(f'Result: {response}')
