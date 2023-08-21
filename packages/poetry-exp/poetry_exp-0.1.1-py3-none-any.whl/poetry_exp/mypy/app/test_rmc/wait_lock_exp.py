from threading import Lock, Thread
import time
lock = Lock()

def refresh(s):
    print('Refresh Request by {0}'.format(s))
    lock.acquire()
    print("Acquired lock by {0}".format(s))
    time.sleep(5)
    print('Refresh completed of {0}'.format(s))
    lock.release()
    print("Release lock by {0}".format(s))


def partial_refresh(s):
    print('Partial Refresh: Request by {0}'.format(s))
    lock.acquire()
    print("Partial Refresh: Acquired lock by {0}".format(s))
    time.sleep(5)
    print('Partial Refresh: Request completed of {0}'.format(s))
    lock.release()
    print("Partial Refresh: Release2 lock by {0}".format(s))

if __name__ == '__main__':
    for i in range(5):
        t1 = Thread(target=refresh, args=("Thread-"+str(i),))
        t1.start()
        t1 = Thread(target=partial_refresh, args=("Thread-" + str(i),))
        t1.start()


"""
OUTPUT:
Refresh Request by Thread-0
Acquired lock by Thread-0
Refresh Request by Thread-1
Refresh Request by Thread-2
Refresh Request by Thread-3
Refresh Request by Thread-4
Refresh completed of Thread-0
Release lock by Thread-0
Acquired lock by Thread-1
Refresh completed of Thread-1
Release lock by Thread-1
Acquired lock by Thread-2
Refresh completed of Thread-2
Release lock by Thread-2
Acquired lock by Thread-3
Refresh completed of Thread-3
Release lock by Thread-3
Acquired lock by Thread-4
Refresh completed of Thread-4
Release lock by Thread-4
"""