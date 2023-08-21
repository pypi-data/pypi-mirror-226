"""
A coroutine is a specialized version of a Python generator function

A coroutine is a function that can suspend its execution before reaching return,
and it can indirectly pass control to another coroutine for some time.
"""

#!/usr/bin/env python3
# countasync.py

import random
import asyncio
loop = asyncio.get_event_loop()



async def count(task_name):
    print("Task: {0}, One".format(task_name))
    # Pause here and come back to count() when sleep() is ready
    await asyncio.sleep(1)
    # awaits kewords tells the event loop that Suspend execution of count() until whatever I am waiting
    # on—the result of sleep()—is returned. In the meantime, go let something else run.
    print("Task: {0}, Two".format(task_name))


async def main():
    await asyncio.gather(count("task1"), count("task2"), count("task3"))


async def get_luckey_number(fun_name):
    #j = input('Waitting for input for fun: {0}'.format(fun_name))
    print('Waitting to get lucky number for fun: {0}'.format(fun_name))
    num = 0
    while True:
        num = random.randint(1,20)
        print(num)
        if num == 10:
            print ('Got the lucky number')
            break
        print("Got number {}, not a lucky number waiting".format(num))
        await asyncio.sleep(1)

    return num


async def fun1():
    print("Executing fun1...")
    num = await get_luckey_number("fun1")
    print ('Number received: {0}'.format(num))
    print('Executed function 1')


async def some_calculation(fun_name):
    print('Doing calculation for fun: {0}'.format(fun_name))
    for i in range(1000):
        j = i * 10
    return j


async def fun2():
    print("Executing fun2...")
    data = await some_calculation("fun2")
    print('Executed function 2, result: {0}'.format(data))
    return data


async def fun3():
    print("Executing fun3...")
    data = await some_calculation("fun3")
    print('Executed function 3, result: {0}'.format(data))
    return data


async def fun4():
    print("Executing fun4...")
    data = await some_calculation("fun4")
    print('Executed fun4, result: {0}'.format(data))
    return data


async def main2():
    await asyncio.gather(fun1(), fun2(), fun3(), fun4())
    # These all function should be independent, can run in any order

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    loop.run_until_complete(main2())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

"""
Task: task2, One
Task: task3, One
Task: task1, One
Task: task2, Two
Task: task3, Two
Task: task1, Two
C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/asyncio_exp/coroutine_exp.py executed in 1.00 seconds.

The order of this output is the heart of async IO. Talking to each of the calls to count() is a single event loop,
or coordinator. When each task reaches await asyncio.sleep(1), the function yells up to the event loop and gives
control back to it, saying, I am  going to be sleeping for 1 second. Go ahead and let something else meaningful be
done in the meantime.
"""