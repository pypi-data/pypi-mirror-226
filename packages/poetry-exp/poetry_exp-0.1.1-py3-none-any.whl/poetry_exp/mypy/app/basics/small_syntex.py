
"""

>>> b[0::2]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'int' object has no attribute '__getitem__'
>>> range(0, b, 2)
[0, 2, 4, 6, 8]
>>> range(0, b+1, 2)
[0, 2, 4, 6, 8, 10]
>>> b=0
>>> range(0, b+1, 2)
[0]
>>> b=1
>>> range(0, b+1, 2)
[0]
>>> b=10
>>> range(0, b+1, 2)
[0, 2, 4, 6, 8, 10]
>>> d={"a":1, "b":2}
>>> {v:k for k,v in d.items()}
{1: 'a', 2: 'b'}
>>> a = {v:k for k,v in d.items()}
>>> a
{1: 'a', 2: 'b'}
>>> def swap(d):
...    return {v:k for k,v in d.items()}
...
>>> swap(d)
{1: 'a', 2: 'b'}
>>> swap({})
{}
>>> def process_hex_string(hs):    sa = hs.split(":")    required_str = sa[1:3]    for i in range(len(required_str)-1, 0, -1):        print required_str[i]
  File "<stdin>", line 1
    def process_hex_string(hs):    sa = hs.split(":")    required_str = sa[1:3]    for i in range(len(required_str)-1, 0, -1):        print required_str[i]
                                                                    ^
SyntaxError: invalid syntax
>>> nl =[1,1]
>>> s=sum([num for num in nl if nl.count(num)==1])
>>> s
0
>>> nl =[]
>>> s=sum([num for num in nl if nl.count(num)==1])
>>> s
0
>>> def g(n):
...   for in in range(n):
  File "<stdin>", line 2
    for in in range(n):
         ^
SyntaxError: invalid syntax
>>> def g(n):
...    for i in range(n):
...       yield i
...
>>> c = g(3)
>>> c.next()
0
>>> for i in c:
...   pass
...
>>> c.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
>>> def mul():
...    return [lambda x: i*x for i in range(4)]
...
>>> print [m(2) for m in mul()]
[6, 6, 6, 6]
>>> [m for m in mul]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'function' object is not iterable
>>> [m for m in mul()]
[<function <lambda> at 0x0000000004AAF128>, <function <lambda> at 0x0000000004AAF198>, <function <lambda> at 0x0000000004AAF208>, <function <lambda> at 0x0000000004AAF2E8>]
>>> yer3

"""




# 1, 1.0 behave as boolean True value in key
d = {True: 'yes', 1: 'no', 1.0: 'maybe'}
print d # {True: 'maybe'}

d={1:"Y", True:"Z"}
print d # {1: "Z"}

# Find most common element
import collections
c = collections.Counter('HelloWorld')
print c.most_common(1)  # [('l', 3)]

# map(function, sequence[, sequence, …])
print map(lambda x, y: x * y, [1, 2, 3], [1, 2, 3])   # [1, 4, 9]
#  map(lambda x:x*x, [1,2,3],[1,2,3])  # error TypeError: <lambda>() takes exactly 1 argument (2 given)


"""
PEP: Python Enhancement Proposal
items =[None]
>>> if items:
...   print 'exist'
... else:
...   print 'Non'
...
exist
>>> len(items)
1


>>> a = all((1, None, "Help!", 42))
>>> a
False


>>> a = all(1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'int' object is not iterable
>>> a = all([10,20,30])
>>> a
True
>>> a = all([10,20,0])
>>> a
False
>>>
"""