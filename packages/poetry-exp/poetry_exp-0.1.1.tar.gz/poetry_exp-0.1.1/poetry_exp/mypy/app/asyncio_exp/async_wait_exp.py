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


async def get_luckey_number(fun_name, lucky_num):
    #j = input('Waitting for input for fun: {0}'.format(fun_name))
    print('Waitting to get lucky number for fun: {0}'.format(fun_name))
    num = 0
    while True:
        num = random.randint(1, 20)
        print(num)
        if num == lucky_num:
            print ('Got the lucky number')
            break
        print("Got number {}, not a lucky number waiting".format(num))
        await asyncio.sleep(1)

    return num


async def some_calculation(fun_name):
    print('Doing calculation for fun: {0}'.format(fun_name))
    for i in range(1000):
        j = i * 10
    return j


async def fun1():
    print("Executing fun1...")
    num = await get_luckey_number("fun1", 10)
    print ('Number received: {0}'.format(num))
    print('Executed function 1')
    return num


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


async def main():
    await asyncio.gather(fun1(), fun2(), fun3(), fun4())
    # These all function should be independent, can run in any order

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    loop.run_until_complete(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

"""
C:\Python3\python.exe "C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/asyncio_exp/coroutine_exp.py"
Executing fun3...
Doing calculation for fun: fun3
Executed function 3, result: 9990
Executing fun1...
Waitting to get lucky number for fun: fun1
13
Got number 13, not a lucky number waiting
Executing fun4...
Doing calculation for fun: fun4
Executed fun4, result: 9990
Executing fun2...
Doing calculation for fun: fun2
Executed function 2, result: 9990
16
Got number 16, not a lucky number waiting
6
Got number 6, not a lucky number waiting
5
Got number 5, not a lucky number waiting
19
Got number 19, not a lucky number waiting
2
Got number 2, not a lucky number waiting
10
Got the lucky number
Number received: 10
Executed function 1
C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/asyncio_exp/coroutine_exp.py executed in 6.02 seconds.

Process finished with exit code 0

"""