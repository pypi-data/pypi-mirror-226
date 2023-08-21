"""
an iterator is an object which implements the iterator protocol, which consist of the methods __iter__() and __next__().
To create an object/class as an iterator you have to implement the methods __iter__() and __next__() to your object.

An object is called iterable if we can get an iterator from it. Most of built-in containers in Python like: list, tuple, string etc. are iterables.
An iterator is an object which will return data, one element at a time.
Python iterator object must implement two special methods, __iter__() and __next__(), collectively called the iterator protocol.
>>> l =[1,2,3]
>>> i = iter(l)
>>> i
<listiterator object at 0x0000000004BA39B0>
>>> next(i)
1
>>> next(i)
2
>>> next(i)
3
>>> next(i)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
>>>

An iterable object can be created by any class. It only needs 3 things: 2 required and one optional.

The two required are:

A method called __iter__ that will return the instance object. A very simple piece of code.
A method called next that will return the next value of the iterable.
These two will create an unbounded or unlimited iterator.

Optionally you might want your iterator to stop at a certain point by itself. You can achieve that by having the next method raise a StopIteration exception.


An iterable is any object in Python which has an __iter__ or a __getitem__ method
defined which returns an iterator or can take indexes (You can read more about them
here). In short an iterable is any object which can provide us with an iterator. So

what is an iterator?
An iterator is any object in Python which has a next (Python2) or __next__ method
defined. Thats it. Thats an iterator. Now lets understand iteration.

Iteration:
In simple words it is the process of taking an item from something e.g a list. When
we use a loop to loop over something it is called iteration. It is the name given to the
process itself. Now as we have a basic understanding of these terms lets understand
generators.
"""

from exceptions import StopIteration

class Counter(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.current = start

    def __iter__(self):
        return self

    def next(self):
        if self.current> self.end:
            raise StopIteration
        else:
           self.current +=1
           return self.current-1


# for i in Counter(10, 20):
#     print i

"""Same behaviour can be achieved using generator function"""

def counter_gen(start, end):
    count = start
    while count<=end:
        yield count
        count += 1

# for j in counter_gen(10, 20):
#     print j


"""Same behaviour can be achieved using generator expression"""


def counter_gen_exp(start, end):
   return (i for i in range(start, end+1))


# for j in counter_gen_exp(10, 20):
#     print j



"""Same behaviour can be achieved using getitem"""

class CustomRange(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __getitem__(self, item):
        if item >= len(self):
            raise IndexError("CustomRange index out of range")
        return self.start + item

    def __len__(self):
        return self.end - self.start


cr = CustomRange(10, 21)
# for i in cr:
#     print(i)


class InfiniteCounter(object):

    def __init__(self, start):
        self.start = start
        self.current = start

    def __iter__(self):
        return self

    def next(self):
       self.current +=1
       return self.current-1


for i in InfiniteCounter(10):
    print (i)
    if i==100:
        break


if __name__ == '__main__':
    c = Counter(1, 10)
    print (c) # <__main__.Counter object at 0x0000000004AF1F98>
    print (iter(c)) # <__main__.Counter object at 0x0000000005671F98>
    for item in c: # this will call the iter on object c which will return iterator object and then it will next on it
        print (item)