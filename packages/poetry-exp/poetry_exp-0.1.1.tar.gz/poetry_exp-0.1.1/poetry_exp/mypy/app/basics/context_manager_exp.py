"""
Context managers are a way of allocating and releasing some sort of resource exactly where you need it

"""

with open('some_dict_facts.py', 'r') as f:
    print f.read()

# Connection will close, because method open returns a file object which is context manager

# Above code similar to following
try:
    f = open('some_dict_facts.py', 'r')
    print f.read()
finally:
    f.close()


# Custom Context Managers
class FileCM(object):
    def __init__(self, file_name, mode):
        self.file_name = file_name
        self.mode = mode

    def __enter__(self):
        print '........entering......'
        self.fd =  open(self.file_name, self.mode)
        return self.fd

    def __exit__(self, exc_type, exc_val, exc_tb):
        print '........exiting......'
        self.fd.close()


with FileCM('some_dict_facts.py', 'r') as f:
    print f.read()
    #a = 3/0  # ZeroDivisionError: integer division or modulo by zero , Still it will close the connection


# E.g 2
import threading

lock = threading.Lock()
with lock:
    lock.acquire()
    print '.................hello...............'
