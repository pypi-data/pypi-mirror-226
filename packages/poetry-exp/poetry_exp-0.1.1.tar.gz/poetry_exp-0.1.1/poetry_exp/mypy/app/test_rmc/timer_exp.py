import datetime, threading
from threading import Timer
timer = None
def fun1(s):
    print "Executing fun1, args: ", s

timer_list = []

def foo():
    print datetime.datetime.now()
    global timer, timer_list
    if not timer:
        print 'comes here'
        timer = Timer(1, foo)
        print dir(timer)
        timer_list.append(timer)
        print timer
        timer.start()
    else:
        timer.cancel()
        del timer
        timer = Timer(1, foo)
        print timer
        timer.start()


foo()


"""
2019-05-24 09:18:15.628000
2019-05-24 09:18:16.629000Executing fun1, args: 
 Hello
2019-05-24 09:18:17.629000
2019-05-24 09:18:18.629000
2019-05-24 09:18:19.629000
2019-05-24 09:18:20.629000
2019-05-24 09:18:21.629000
2019-05-24 09:18:22.629000
2019-05-24 09:18:23.629000
2019-05-24 09:18:24.629000
2019-05-24 09:18:25.630000
2019-05-24 09:18:26.631000
2019-05-24 09:18:27.632000
2019-05-24 09:18:28.633000
2019-05-24 09:18:29.633000
"""


