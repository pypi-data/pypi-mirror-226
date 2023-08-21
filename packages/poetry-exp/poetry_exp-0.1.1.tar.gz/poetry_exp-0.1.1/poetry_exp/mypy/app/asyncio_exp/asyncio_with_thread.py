import asyncio
import threading
import time


async def task1():
    for i in range(10):
        await asyncio.sleep(1)
        print(f'Running i: {i}')
    print('Completed task1')
    return 1


async def call_task1():
    # await asyncio.sleep(1)
    n = await task1()
    return n


def execute_tasks(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(call_task1())


if __name__ == '__main__':
    # create a new event loop in the main thread
    loop = asyncio.new_event_loop()

    # Calling corutine(call_task1) in a thread
    thread = threading.Thread(target=execute_tasks, args=(loop,))
    thread.start()
    print(f"end main thread")


"""
it's generally not recommended to mix asyncio and threads in this way.
It can be difficult to manage the synchronization of the event loop and thread,
and can lead to performance issues. It's usually better to stick to either asyncio
or threads, depending on the nature of your application.

Again, while this is technically possible, it's generally not recommended as it
can lead to synchronization and performance issues
"""