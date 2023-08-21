"""
A coroutine is a specialized version of a Python generator function

A coroutine is a function that can suspend its execution before reaching return,
and it can indirectly pass control to another coroutine for some time.
"""

#!/usr/bin/env python3
# countasync.py

import asyncio
import os
loop = asyncio.get_event_loop()


async def ping_server(server_ip, ping_time, ping_details, max_attempt=3):
    print('*******************Pinging server {0}'.format(server_ip))
    ping_result = -1
    attempt = 0
    ping_details[server_ip] = False
    while attempt < max_attempt:
        ping_result = os.system("ping -c 1 " + server_ip)
        if ping_result == 0:
            ping_details[server_ip] = True
            print('Server {0} is now reachable'.format(server_ip))
            break

        attempt += 1
        print('Attempt: {0}'.format(attempt))
        if attempt >= max_attempt:
            print('!!!!!!!!!!!!!!Max attempt reached, stopped pinging')
            break

        print("####Server: {0} not reachable, will ping after {1} sec again, attempt: {2}".format(server_ip, ping_time, attempt))
        await asyncio.sleep(ping_time)

    return ping_result


async def ping_servers():
    servers = ['google.com', '172.17.29.162', 'python.org']
    tasks = []
    ping_details = {}
    for server in servers:
        task = ping_server(server, 0.2, ping_details)
        tasks.append(task)
    await asyncio.gather(*tasks)  # These all function should be independent, can run in any order
    print('Servers Ping Result: {0}'.format(ping_details))


if __name__ == "__main__":
    import time
    s = time.perf_counter()
    loop.run_until_complete(ping_servers())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

"""
C:\Python3\python.exe "C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/asyncio_exp/ping_server_exp.py"
*******************Pinging server python.org

Pinging python.org [45.55.99.72] with 32 bytes of data:
Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 45.55.99.72:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
Attempt: 1
####Server: python.org not reachable, will ping after 0.2 sec again, attempt: 1
*******************Pinging server google.com

Pinging google.com [64.233.177.113] with 32 bytes of data:
Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 64.233.177.113:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
Attempt: 1
####Server: google.com not reachable, will ping after 0.2 sec again, attempt: 1
*******************Pinging server 172.17.29.162

Pinging 172.17.29.162 with 32 bytes of data:
Request timed out.
Request timed out.
Reply from 172.17.29.162: bytes=32 time=2ms TTL=63
Reply from 172.17.29.162: bytes=32 time=3ms TTL=63

Ping statistics for 172.17.29.162:
    Packets: Sent = 4, Received = 2, Lost = 2 (50% loss),
Approximate round trip times in milli-seconds:
    Minimum = 2ms, Maximum = 3ms, Average = 2ms
Server 172.17.29.162 is now reachable

Pinging python.org [45.55.99.72] with 32 bytes of data:
Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 45.55.99.72:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
Attempt: 2
####Server: python.org not reachable, will ping after 0.2 sec again, attempt: 2

Pinging google.com [64.233.177.113] with 32 bytes of data:
Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 64.233.177.113:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
Attempt: 2
####Server: google.com not reachable, will ping after 0.2 sec again, attempt: 2

Pinging python.org [45.55.99.72] with 32 bytes of data:
Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 45.55.99.72:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
Attempt: 3
!!!!!!!!!!!!!!Max attempt reached, stop poinging

Pinging google.com [64.233.177.113] with 32 bytes of data:
Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 64.233.177.113:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
Attempt: 3
!!!!!!!!!!!!!!Max attempt reached, stop poinging
Servers Ping Result: {'python.org': False, 'google.com': False, '172.17.29.162': True}
C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/asyncio_exp/ping_server_exp.py executed in 125.59 seconds.

Process finished with exit code 0


"""