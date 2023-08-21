import time
from multiprocessing import Process


def fun(i):
    a = []
    for j in range(5):
      print 'Executing Thread: ', str(i)
      a.append(' ' * 10 ** 6)
      time.sleep(1)
    print 'Finished Thread: ', str(i)

jobs = []
for i in range(10):
    p = Process(target=fun, args=(i,))
    jobs.append(p)
    p.start()

for job in jobs:
    job.join()

for job in jobs:
    print 'Terminating process: ', job.pid
    job.terminate()


