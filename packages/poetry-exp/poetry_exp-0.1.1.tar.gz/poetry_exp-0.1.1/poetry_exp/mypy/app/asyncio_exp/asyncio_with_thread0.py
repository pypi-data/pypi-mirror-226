import asyncio
import threading

async def my_coroutine():
    # do some async work
    await asyncio.sleep(1)
    print("Async task completed")

def my_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(my_coroutine())


if __name__ == '__main__':
    # create a new event loop in the main thread
    loop = asyncio.new_event_loop()

    # start a new thread and pass the event loop as an argument
    thread = threading.Thread(target=my_thread, args=(loop,))
    thread.start()

    # run the event loop in the main thread
    #loop.run_forever()

    # wait for the thread to complete
    thread.join()




"""
it's generally not recommended to mix asyncio and threads in this way.
It can be difficult to manage the synchronization of the event loop and thread,
and can lead to performance issues. It's usually better to stick to either asyncio
or threads, depending on the nature of your application.

Again, while this is technically possible, it's generally not recommended as it
can lead to synchronization and performance issues
"""