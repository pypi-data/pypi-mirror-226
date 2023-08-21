import Queue
import threading
import urllib2
import time

# called by each thread
def get_url(q, url):
    q.put(urllib2.urlopen(url).read())

def thread_fun(q, x):
   q.put(printx(x))

def printx(x):
  time.sleep(5)
  print "x is ",x

def printxy(x, y):
  print "x=%s and y=%s " % (x,y)


def worker():
    """thread worker function"""
    print 'Worker'
    return

def worker2(num):
    """thread worker function"""
    print 'Worker: %s' % num
    return

threads = []
for i in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

threads = []
for i in range(5):
    t = threading.Thread(target=worker2, args=(i,))
    threads.append(t)
    t.start()

t3 = threading.Thread(target=printx, args = (10,))


#printx will stoppped it is not finished within main thread
#won't keep the process up if main thread ends 
t3.daemon = True
t3.start()

t4 = threading.Thread(target=printxy, args =(10,20))
print t4.daemon
t4.start()


"""
theurls = ["http://google.com", "http://yahoo.com"]

q = Queue.Queue()
for u in theurls:
    t = threading.Thread(target=get_url, args = (q,u))
    t.daemon = True
    t.start()

s = q.get()
print s


This is a case where threading is used as a simple optimization: each subthread is waiting for a URL to resolve and respond,
 in order to put its contents on the queue; each thread is a daemon (won't keep the process up if main thread ends
  -- that's more common than not); the main thread starts all subthreads,
   does a get on the queue to wait until one of them has done a put, then emits the results and terminates
    (which takes down any subthreads that might still be running, since they're daemon threads).

Proper use of threads in Python is invariably connected to I/O operations 
(since CPython doesn't use multiple cores to run CPU-bound tasks anyway,
 the only reason for threading is not blocking the process while there's a wait for some I/O).
  Queues are almost invariably the best way to farm out work to threads and/or collect the works results,
   by the way, and they're intrinsically threadsafe so they save you from worrying about locks,
    conditions, events, semaphores, and other inter-thread coordination/communication concepts.
"""
