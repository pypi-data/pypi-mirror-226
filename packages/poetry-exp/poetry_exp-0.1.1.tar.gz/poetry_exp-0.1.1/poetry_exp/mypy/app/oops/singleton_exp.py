import threading


class ThreadSafeSingleton(type):
    _instances = {}
    _singleton_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            print('Instance not found')
            with cls._singleton_lock:
                if cls not in cls._instances:
                    print('Creating Instance...')
                    cls._instances[cls] = super(ThreadSafeSingleton, cls).\
                        __call__(*args, **kwargs)
        else:
            print('Instance found')
        return cls._instances[cls]


class Test(metaclass=ThreadSafeSingleton):

    def __init__(self, name):
        print(f"Initializing: {name}")  # will execute only once


if __name__ == '__main__':
    ts1 = Test("ts1")
    ts2 = Test("ts2")
    ts3 = Test("ts3")
    print(f'ts1:{id(ts1)}, ts2:{id(ts2)}, ts3:{id(ts3)}')

"""
Instance not found
Creating Instance...
Initializing: ts1
Instance found
Instance found
ts1:81030160, ts2:81030160, ts3:81030160
"""