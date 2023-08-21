"""
collections module was introduced to improve the functionality of the built-in datatypes.
It provides various containers let’s see each one of them in detail.

Counter: sub-class of the dictionary. It is used to keep the count of the elements in an iterable
in the form of an unordered dictionary where the key represents the element in the iterable and
value represents the count of that element in the iterable.

>>> votes = ['SP','BJP','SP','SP','AAP','BJP','AAP','AAP']
>>> vote_counts = Counter(votes)
>>> vote_counts
Counter({'SP': 3, 'AAP': 3, 'BJP': 2})

>>> vote_counts.update(['BJP', 1])
>>> vote_counts
Counter({'SP': 3, 'BJP': 3, 'AAP': 3, 1: 1})
>>> vote_counts.update(['BJP','BJP', 5])
>>> vote_counts
Counter({'BJP': 5, 'SP': 3, 'AAP': 3, 1: 1, 5: 1})
>>>
>>> vote_counts.pop(1)
1
>>> vote_counts
Counter({'BJP': 5, 'SP': 3, 'AAP': 3, 5: 1})
>>> vote_counts.pop(5)
1
>>> vote_counts
Counter({'BJP': 5, 'SP': 3, 'AAP': 3})
>>> vote_counts.popitem('AAP')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: popitem() takes no arguments (1 given)
>>> vote_counts.popitem()
('AAP', 3)
>>>



OrderedDict: is also a sub-class of dictionary but unlike a dictionary, it remembers the order
in which the keys were inserted.

>>> from collections import OrderedDict
>>> od=OrderedDict()
>>> od['a']=1
>>> od['b']=2
>>> od['c']=3
>>> od
OrderedDict([('a', 1), ('b', 2), ('c', 3)])
>>>
>>> for k, v in od.items():
...   print(k, v)
...
a 1
b 2
c 3
>>>


defaultdict: is used to provide some default values for the key that does not exist and never raises a KeyError.
Its objects can be initialized using DefaultDict() method by passing the data type as an argument

Note: default_factory is a function that provides the default value for the dictionary created.
If this parameter is absent then the KeyError is raised.
>>> d=defaultdict()
>>> d['name']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'name'
>>> d=defaultdict(str)
>>> d['name']
''
>>> d=defaultdict(int)
>>> d['age']
0
>>> d=defaultdict(defaultdict)
>>> d['address']
defaultdict(None, {})
>>> d['address']['city']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'city'
>>>


ChainMap: encapsulates many dictionaries into a single unit and returns a list of dictionaries.
When a key is needed to be found then all the dictionaries are searched one by one until the key is found.
>>> from collections import ChainMap
>>> d1={'a':1,'b':2}
>>> d2={'c':3,'d':4}
>>> d3={'e':5,'f':6, 'a':1.0,'d':4.0}
>>> cm=ChainMap(d1,d2,d3)
>>> cm
ChainMap({'a': 1, 'b': 2}, {'c': 3, 'd': 4}, {'e': 5, 'f': 6, 'a': 1.0, 'd': 4.0})
>>> cm['a']
1 # will not overwrite with 1.0, since key 'a' founds early in the first dict d1
>>> cm['d']
4
>>>
>>> for c in cm.items():
...   print(c)
...
('d', 4)
('f', 6)
('a', 1)
('b', 2)
('c', 3)
('e', 5)
              ^
>>> cm['a']=1.1
>>> cm['a']
1.1
>>> cm
ChainMap({'a': 1.1, 'b': 2}, {'c': 3, 'd': 4}, {'e': 5, 'f': 6, 'a': 1.0, 'd': 4.0})
>>>



namedtouple: returns a tuple object with names for each position which the ordinary tuples lack.
So we don't need to remember the indices like o,1 ect.
For example, consider a tuple names student where the first element represents fname, second represents lname
and the third element represents the DOB. Suppose for calling fname instead of remembering the index
position you can actually call the element by using the fname argument, then it will be really easy for
accessing tuples element. This functionality is provided by the NamedTuple.
>>> from collections import namedtuple
>>> Emp = namedtuple("Employee", ('name','age', 'salary'))
>>> e2 = Emp('B',30,300000)
>>> e1 = Emp('A',20,200000)
>>> e1
Employee(name='A', age=20, salary=200000)
>>> e2
Employee(name='B', age=30, salary=300000)
>>>
>>> e1.name
'A'
>>> e1.age
20
>>>
>>> e1[0]
'A'
>>> e1[1]
20
>>>
>>> type(e1)
<class '__main__.Employee'>
>>>
>>> for i in e1:
...   print(i)
...
A
20
200000
>>>
"""