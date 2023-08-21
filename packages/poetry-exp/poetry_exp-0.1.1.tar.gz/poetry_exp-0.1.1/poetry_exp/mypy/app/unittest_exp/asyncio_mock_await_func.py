import asyncio
from datetime import datetime


async def stop_after(loop, when):
    await asyncio.sleep(when)
    print("Time: {0}, Stopping the loop".format(datetime.now()))
    loop.stop()


async def execute_task1(data):
    print("Executing task1...")
    await asyncio.sleep(1)


async def start_worker(data):
    print("starting worker....")
    await execute_task1(data)


if __name__ == '__main__':
    data = {"a":1}
    loop = asyncio.get_event_loop()
    loop.create_task(start_worker(data))
    loop.create_task(stop_after(loop, 2))
    loop.run_forever()
    loop.close()


