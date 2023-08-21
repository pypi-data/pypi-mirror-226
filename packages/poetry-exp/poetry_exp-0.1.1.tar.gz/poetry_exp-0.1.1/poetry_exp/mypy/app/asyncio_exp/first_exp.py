import asyncio


async def my_coroutine():
    print("Running my_coroutine")
    # This is not mandatory, without await also coroutine can be
    # defined but will behave like normal function, await is use to suspend the
    # exection(in this case sleep) till the function completes and switch to other coroutine
    await asyncio.sleep(1)
    print("Done with my_coroutine")

"""
A coroutine is simply a special type of Python generator that allows you to suspend
and resume its execution using the await keyword.

The await keyword is used to suspend the execution of a coroutine until a particular 
operation completes. However, it is not necessary to use await in a coroutine if you do not need 
to suspend its execution.
"""

if __name__ == '__main__':
    # In a typical Python application that uses the asyncio module, you should generally only
    # have one event loop running per thread.
    loop = asyncio.get_event_loop()

    coro_obj = my_coroutine()  # Call the coroutine without await

    task = loop.create_task(coro_obj)  # Schedule the coroutine to run

    loop.run_until_complete(task)


"""
In this code, we first define a coroutine called my_coroutine(). We then create an event
loop and call the my_coroutine() function without await, which returns a coroutine object.
We then schedule this coroutine to run on the event loop using loop.create_task(),
which returns a Task object that represents the coroutine's execution.

Finally, we run the event loop until the coroutine has completed using loop.run_until_complete().
When the event loop starts, it runs the coroutine, prints "Running my_coroutine", sleeps for 1
second using asyncio.sleep(), and then prints "Done with my_coroutine".

Note that calling a coroutine without await is not a common pattern in asyncio programming,
as it can be confusing and lead to unexpected behavior if not used carefully. It is generally
better to use await to run coroutines and schedule them on the event loop.


"""