#!/usr/bin/env python3
# countasync.py

import asyncio
loop = asyncio.get_event_loop()

async def count(task_name):
    print("Task: {0}, One".format(task_name))
    await asyncio.sleep(1)
    print("Task: {0}, Two".format(task_name))

async def main():
    await asyncio.gather(count("task1"), count("task2"), count("task3"))

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    loop.run_until_complete(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")