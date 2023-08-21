import asyncio
import time
import datetime
loop = asyncio.get_event_loop()

async def run_command(cmd):
    process = await asyncio.create_subprocess_exec(cmd, stdout=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return stdout.decode().strip()


async def run_commands(cmds):
    tasks = []
    for cmd in cmds:
        task = loop.create_task(run_command(cmd))
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    cmds = ['ipconfig', 'date']
    s = time.perf_counter()
    results = loop.run_until_complete(run_commands(cmds))
    for result in results:
        print(result)
    total_time = time.perf_counter() - s
    print('{0}: total_time: {1}'.format(datetime.now(), total_time))








"""
import asyncio
async def run_command(*args):
    # Create subprocess
    process = await asyncio.create_subprocess_exec(
        *args,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE)
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    # Return stdout
    return stdout.decode().strip()


loop = asyncio.get_event_loop()
# Gather uname and date commands
commands = asyncio.gather(run_command('uname'), run_command('date'))
# Run the commands
uname, date = loop.run_until_complete(commands)
# Print a report
print('uname: {}, date: {}'.format(uname, date))
loop.close()

"""