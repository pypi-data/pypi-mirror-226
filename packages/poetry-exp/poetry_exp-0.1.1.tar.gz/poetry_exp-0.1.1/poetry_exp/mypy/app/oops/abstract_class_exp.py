
"""
Py2:
>>> dir(abc)
['ABCMeta', 'WeakSet', '_C', '_InstanceType', '__builtins__', '__doc__', '__file__', '__name__', '__package__',
 'abstractmethod', 'abstractproperty', 'types']
>>>
Py3:
>>> from abc import ABC
>>> import abc
>>> dir(abc)
['ABC', 'ABCMeta', 'WeakSet', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__',
 '__package__', '__spec__', 'abstractclassmethod', 'abstractmethod', 'abstractproperty', 'abstractstaticmethod',
  'get_cache_token']
>>>
"""

from abc import abstractmethod

class Base(object):
    @abstractmethod
    def fun1(self):
        pass

class Emp(Base):
    def __init__(self, name):
        self.name=name

if __name__ == '__main__':
    e = Emp("a")
    print e.fun1()

