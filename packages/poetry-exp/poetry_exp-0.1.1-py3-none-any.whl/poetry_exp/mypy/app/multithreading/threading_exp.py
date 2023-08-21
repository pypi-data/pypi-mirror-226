#!/usr/bin/python


""""
The Threading Module:

The newer threading module included with Python 2.4 provides much more powerful, high-level support for threads
 than the thread module discussed in the previous section.

The threading module exposes all the methods of the thread module and provides some additional methods:

  threading.activeCount(): Returns the number of thread objects that are active.

  threading.currentThread(): Returns the number of thread objects in the caller's thread control.

  threading.enumerate(): Returns a list of all thread objects that are currently active.

In addition to the methods, the threading module has the Thread class that implements threading.
The methods provided by the Thread class are as follows:

  run(): The run() method is the entry point for a thread.

  start(): The start() method starts a thread by calling the run method.

  join([time]): The join() waits for threads to terminate.

  isAlive(): The isAlive() method checks whether a thread is still executing.

  getName(): The getName() method returns the name of a thread.

  setName(): The setName() method sets the name of a thread.




"""


from threading import Thread
import time

exitFlag = 0


class myThread(Thread):
    def __init__(self, threadID, name, counter):
        Thread.__init__(self, name=name)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name


def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1


# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

thread1.join()
thread2.join()

print "Exiting Main Thread"



"""
Starting Thread-1
Starting Thread-2
Thread-1: Wed Jul 11 21:52:52 2018
Thread-1: Wed Jul 11 21:52:53 2018Thread-2: Wed Jul 11 21:52:53 2018

Thread-1: Wed Jul 11 21:52:54 2018
Thread-2: Wed Jul 11 21:52:55 2018
Thread-1: Wed Jul 11 21:52:55 2018
Thread-1: Wed Jul 11 21:52:56 2018
Exiting Thread-1
Thread-2: Wed Jul 11 21:52:57 2018
Thread-2: Wed Jul 11 21:52:59 2018
Thread-2: Wed Jul 11 21:53:01 2018
Exiting Thread-2
Exiting Main Thread
"""