"""
https://www.quantstart.com/articles/Parallelising-Python-with-Threading-and-Multiprocessing
Multiprocessing refers to the ability of a system to support more than one processor at the same time.
 Applications in a multiprocessing system are broken to smaller routines that run independently.
  The operating system allocates these threads to the processors improving performance of the system.

Why multiprocessing?

Consider a computer system with a single processor. If it is assigned several processes at the same time,
 it will have to interrupt each task and switch briefly to another, to keep all of the processes going.
This situation is just like a chef working in a kitchen alone. He has to do several tasks like baking,
 stirring, kneading dough, etc.

 So the gist is that: The more tasks you must do at once, the more difficult it gets to keep track of them all,
  and keeping the timing right becomes more of a challenge.
This is where the concept of multiprocessing arises!
A multiprocessing system can have:

multiprocessor, i.e. a computer with more than one central processor.
multi-core processor, i.e. a single computing component with two or more independent actual processing units (called cores).
Here, the CPU can easily executes several tasks at once, with each task using its own processor.

It is just like the chef in last situation being assisted by his assistants.
 Now, they can divide the tasks among themselves and chef doesnt need to switch between his tasks.

Multiprocessing in Python

In Python, the multiprocessing module includes a very simple and intuitive API for dividing work between multiple processes.
Using threading module:
time python thread_test.py
It produces the following output:

List processing complete.

real    0m2.003s
user    0m1.838s
sys     0m0.161s

Using multiprocessing module:
In order to actually make use of the extra cores present in nearly all modern consumer processors
 we can instead use the Multiprocessing library. This works in a fundamentally different way to the
  Threading library, even though the syntax of the two is extremely similar.

The Multiprocessing library actually spawns multiple operating system processes for each parallel task.
 This nicely side-steps the GIL, by giving each process its own Python interpreter and thus own GIL.
  Hence each process can be fed to a separate processor core and then regrouped at the end once all processes have finished.

There are some drawbacks, however. Spawning extra processes introduces I/O overhead as data is having
 to be shuffled around between processors. This can add to the overall run-time. However, assuming the data
  is restricted to each process, it is possible to gain significant speedup

time python multiproc_test.py
We receive the following output:

List processing complete.

real    0m1.045s
user    0m1.824s
sys     0m0.231s
In this case you can see that while the user and sys times have reamined approximately the same,
the real time has dropped by a factor of almost two. This makes sense since we're using two processes.
Scaling to four processes while halving the list size for comparison gives the following output
 (under the assumption that you have at least four cores!):

List processing complete.

real    0m0.540s
user    0m1.792s
sys     0m0.269sBashCopy
This is an approximate 3.8x speed-up with four processes. However, we must be careful of generalising this
 to larger, more complex programs. Data transfer, hardware cache-levels and other issues will almost certainly
  reduce this sort of performance gain in "real" codes.


"""
import threading
import random
import multiprocessing
import time


def task(out_list):
    for i in range(10000000):
        out_list.append(random.random())


def do_task_using_threading(out_list):
    jobs = []
    for i in range(2):
        t = threading.Thread(target=task, args=(out_list,))
        jobs.append(t)

    for job in jobs:
        job.start()

    for job in jobs:
        job.join()


def do_task_using_multiprocessing(out_list):
    jobs =[]
    for i in range(2):
        p = multiprocessing.Process(target=task, args=(out_list,))
        jobs.append(p)

    for job in jobs:
        job.start()

    for job in jobs:
        job.join()



if __name__ == '__main__':
    output_list = list()
    start = time.time()
    do_task_using_threading(output_list)
    end = time.time()
    print 'Total time taken using thread: ', (end-start) # 20.0730001926 sec

    # start = time.time()
    # do_task_using_multiprocessing(out_list)
    # end = time.time()
    # print 'Total time taken using multiprocess: ', (end-start) # 2.60300016403 sec

# Note: Don't use both approaches at the same time, you may get different behaviour
