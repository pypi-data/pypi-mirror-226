from concurrent.futures import ProcessPoolExecutor
from time import sleep

from multiprocessing import Manager
def fun1(message):
    print("Executing fun1")
    sleep(5)
    message['msg'] = "hello"
    print("executing fun1 done")
    return message

def fun2(message):
    print("Executing fun2")
    sleep(5)
    message['msg2'] = "hello2"
    print("executing fun2 done")
    return message


pool = ProcessPoolExecutor(3)
d = Manager().dict()
future = pool.submit(fun1, (d))
f2 = pool.submit(fun2, (d))
#print(future.done())
#sleep(5)
#print(future.done())
print("Result: {0}".format(future.result()))
a = f2.result()
print(d)
