"""
The values in a dictionary can be any type. The keys can be any immutable type.
An object can be a key in a dictionary if it is hashable. ... All of Python's immutable built-in objects are hashable,
Objects which are instances of user-defined classes are hashable by default; their hash value is their id()

mutable, meaning you can change their content without changing their identity.
 Other objects like integers, floats, strings and tuples are objects that can not be changed
"""

d = {'a': 1, '1.2': 1, '1': 123, (10, 20): 30}
print d
"""
d={'a': 1, '1.2':1, '1':123, (10,20): 30, [10, 20]:30} # error

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
>>>
"""


# Get/remove the first item from dict
first = d.popitem()
print first # ('a', 1)
print d  # {'1': 123, (10, 20): 30, '1.2': 1}

# Get/remove the item from a dict by key
item = d.pop('1')
print item  # 123
print d  # {(10, 20): 30, '1.2': 1}


# merge Two dict
d1 = {"a":1}
d2 = {"b":2, "a":3}
d1.update(d2)
print 'Merged dict: ', d1  # {'a': 3, 'b': 2}
print 'has key a: ', d1.has_key("a")


# Compare two dict
d1 = {"a":1, "b":2}
d2 = {"b":2, "a":1}
print d1==d2  # True
print cmp(d1, d2)  # 0
d2 = {"a":1, "b":2, "c":3}
print cmp(d1, d2)  # -1

d1 = {"a":1, "b":"abc", "c": [1,2,3], "d": (1,2,3), "e": {1,2,3}, "f":{"a":1}, (1,2,3):1}
d2 = {"a":1, "b":"abc", "c": [1,2,3], "d": (1,2,3), "e": {1,2,3}, "f":{"a":1}, (1,2,3):1}
print "Compareing dict....., ", d1==d2  # True
eq = True
for k in d1.keys():
    if not (k in d2 and d1.get(k)==d2.get(k)):
        eq = False
        break;
print "Compareing dict. own...., ", eq # True

# Find common element in dict
d1 = {"a":1, "b":2}
d2 = {"c": 3, "b":2, "a":1}
print "common element..... ", {k:v for k, v in d1.items() if k in d2 and d1[k]==d2[k]} # {'a': 1, 'b': 2}

# Dict comp
n =10
d = {x:x*x for x in range(1,n+1)}


# Form the dict from class
class A(object):
    def __init__(self):
        self.A = 1
        self.B = 2
obj = A()
print(obj.__dict__) # {'A': 1, 'B': 2}


# sort list having dict objects by a key
l = [
    {
        "name": "rice",
        "price": 50
    },
    {
        "name": "ice",
        "price": 20
    },
    {
        "name": "tea",
        "price": 10
    }
]
import copy
l2 = copy.copy(l)
l.sort(key=lambda d: d['name'])
print l # [{'price': 20, 'name': 'ice'}, {'price': 50, 'name': 'rice'}, {'price': 10, 'name': 'tea'}]

l.sort(key=lambda d: d['price'])
print l  # [{'price': 10, 'name': 'tea'}, {'price': 20, 'name': 'ice'}, {'price': 50, 'name': 'rice'}]

print l2 # [{'price': 50, 'name': 'rice'}, {'price': 20, 'name': 'ice'}, {'price': 10, 'name': 'tea'}]

# sort without using lambda
for i in range(len(l2)):
    for j in range(i+1, len(l2)):
        if l2[i]['price'] > l2[j]['price']:
            l2[j]['price'], l2[i]['price'] = l2[i]['price'], l2[j]['price']

print l2 # [{'price': 10, 'name': 'rice'}, {'price': 20, 'name': 'ice'}, {'price': 50, 'name': 'tea'}]

# Todo IF Price are same sort by name

# Map two list into dict
alphabet = ['a', 'b', 'c']
mirror = ['z', 'y', 'x']
print dict(zip(alphabet, mirror)) # {'a': 'z', 'c': 'x', 'b': 'y'}