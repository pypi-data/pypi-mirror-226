from concurrent.futures import ProcessPoolExecutor
import threading
import random
#1-44197723209

class MyTask:

   def task(self, name, number, config, logger):
        print("Executing our Task: "+name)
        result = 0
        i = 0
        for i in range(10):
            result = result + i
        print("I: {}".format(result))
        print("Task Executed {}".format(threading.current_thread()))

class Abc2():
   def __init__(self):
       self.l1 = ""
       self.l2 = []
       self.l3 = {}
       print("test abc2")

class Test(object):
    def __init__(self, config, logger):
        self.executor = ProcessPoolExecutor(max_workers=3)
        self.log = Abc2()
        self.a = object() 
        self.logger = logger
        self.config = config

    def main(self):
       mt = MyTask()
       task1 = self.executor.submit(mt.task, "A",1, self.config, self.logger)
       task2 = self.executor.submit(mt.task, "b",2, self.config, self.logger)

if __name__ == '__main__':

    
    t = Test('config', 'logger')
    t.main()

#524440 initial
#aafak2@aafak-ubuntu:~/repos/iei-simple-visualizer$ cat /proc/9994/statm



"""
Note: Python is not thread safe, so to use object in thread safe way, it uses GIL, which make sure only one thread
If max_workers is None or not given, it will default to the number of processors on the machine, multiplied by 5, assuming that ThreadPoolExecutor is often used to overlap I/O instead of CPU work and the number of workers should be higher than the number of workers for ProcessPoolExecutor.

ProcessPool is for CPU bound tasks so you can benefit from multiple CPU.

Threads is for io bound tasks so you can benefit from io wait.

There are some drawbacks of multiprocessing, however. Spawning extra processes introduces I/O overhead as data is having to be shuffled around between processors. This can add to the overall run-time. However, assuming the data is restricted to each process, it is possible to gain significant speedup. Of course, one must always be aware of Amdahl's Law!




ProcessPoolExecutor runs each of your workers in its own separate child process.

ThreadPoolExecutor runs each of your workers in separate threads within the main process.

The Global Interpreter Lock (GIL) doesn't just lock a variable or function; it locks the entire interpreter. This means that every builtin operation, including things like listodicts[3]['spam'] = eggs, is automatically thread-safe.

But it also means that if your code is CPU-bound (that is, it spends its time doing calculations rather than, e.g., waiting on network responses), and not spending most of its time in an external library designed to release the GIL (like NumPy), only one thread can own the GIL at a time. So, if you've got 4 threads, even if you have 4 or even 16 cores, most of the time, 3 of them will be sitting around waiting for the GIL. So, instead of getting 4x faster, your code gets a bit slower.

Again, for I/O-bound code (e.g., waiting on a bunch of servers to respond to a bunch of HTTP requests you made), threads are just fine; it's only for CPU-bound code that this is an issue.

Each separate child process has its own separate GIL, so this problem goes away—even if your code is CPU-bound, using 4 child processes can still make it run almost 4x as fast.

But child processes don't share any variables. Normally, this is a good thing—you pass (copies of) values in as the arguments to your function, and return (copies of) values back, and the process isolation guarantees that you're doing this safely. But occasionally (usually for performance reasons, but also sometimes because you're passing around objects that can't be copied via pickle), this is not acceptable, so you either need to use threads, or use the more complicated explicit shared data wrappers in the multiprocessing module.

"""
