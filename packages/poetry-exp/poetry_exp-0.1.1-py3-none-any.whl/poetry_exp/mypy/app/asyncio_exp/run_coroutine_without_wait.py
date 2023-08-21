import asyncio

async def my_coroutine():
    print('Running coroutine...')
    for i in range(10):
        print(f'Running coroutine: {i}/10')
        await asyncio.sleep(1)


async def par_coroutine():
    print(f'Doing some work...')
    asyncio.ensure_future(my_coroutine())
    print(f'Continue Doing some work after calling coroutine...')
    return "task_id_1"


async def main():
    # If you call without await, it will not call the method, it will simply return a object
    task_id = await par_coroutine()
    print(f"Task created with task_id: {task_id}")
    await asyncio.sleep(20)
    return task_id


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

