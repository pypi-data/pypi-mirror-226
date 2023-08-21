import threading


class ReadWriteLock(object):
    """
    A class to implement locking which allows unlimited read access
    when it is not being modified while keeping write access exclusive
    """

    def __init__(self):
        self.readers_only = threading.Condition(threading.Lock())
        self.readers_count = 0

    def acquire_read(self):
        with self.readers_only:
            self.readers_count += 1

    def release_read(self):
        with self.readers_only:
            self.readers_count -= 1
            if not self.readers_count:
                self.readers_only.notify_all()

    def acquire_write(self):
        self.readers_only.acquire()
        while self.readers_count > 0:
            self.readers_only.wait()

    def release_write(self):
        self.readers_only.release()


class ThreadSafeDict(dict):
    """
    An implementation of RMC dict where allows unlimited read access
    when it is not being modified while keeping write access exclusive
    """

    def __init__(self, **kwargs):
        self.read_write_lock = ReadWriteLock()
        super(ThreadSafeDict, self).__init__(**kwargs)

    def get(self, k, d=None):
        self.read_write_lock.acquire_read()
        try:
            return super(ThreadSafeDict, self).get(k, d)
        finally:
            self.read_write_lock.release_read()

    def update(self, E=None, **F):
        self.read_write_lock.acquire_write()
        try:
            super(ThreadSafeDict, self).update(E)
        finally:
            self.read_write_lock.release_write()

    def pop(self, k, d=None):
        self.read_write_lock.acquire_write()
        try:
            super(ThreadSafeDict, self).pop(k, d)
        finally:
            self.read_write_lock.release_write()

    def __getitem__(self, item):
        self.read_write_lock.acquire_read()
        try:
            return super(ThreadSafeDict, self).__getitem__(item)
        finally:
            self.read_write_lock.release_read()


if __name__ == '__main__':
    d = ThreadSafeDict()
    d['a'] = 1
    print(d)
    print(d['a'])

    # explore it with different threads
