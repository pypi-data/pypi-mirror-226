import time
import threading


def fun(i):
    a = []
    for i in range(10):
      print 'Executing Thread: ', str(i)
      a.append(' ' * 10 ** 6)
      time.sleep(1)
    print 'Finished Thread: ', str(i)


def fun2():
  while True:
      time.sleep(1)
      print ' i am always up'


t = threading.Thread(target=fun2)
t.start()


for i in range(10):
    t = threading.Thread(target=fun, args=(i,))
    t.start()
    t.join()




