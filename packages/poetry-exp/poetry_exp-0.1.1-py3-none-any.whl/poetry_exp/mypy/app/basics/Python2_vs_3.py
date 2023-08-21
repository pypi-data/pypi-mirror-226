"""
Following are the main differences between Py2.x and Py3.x

1. Division operator
2. print function - In Py2 print is treated as a statement rather than a function, Extra pair or parenthesis needed in Py3
3. Unicode - In Python 2, implicit str type is ASCII. But in Python 3.x implicit str type is Unicode.
4. xrange -  In Python 3.x, the range function is similar to xrange Python 2.x
5. Error Handling - except NameError as err: # 'as' keyword is needed in Python 3.x and following will not work in p3
raise IOError, your error message
6. _future_ module - Help in migration/porting our code to python3.x

7. Calling super:

This works in Python 2 and 3:
super(Child, self).__init__()
This only works in Python 3:
super().__init__()
It works with no arguments by moving up in the stack frame and getting the first argument
to the method (usually self for an instance method or cls for a class method
but could be other names) and finding the class (e.g. Child) in the free variables
(it is looked up with the name __class__ as a free closure variable in the method).
I prefer to demonstrate the cross-compatible way of using super,
but if you are only using Python 3, you can call it with no arguments.

py3: super().methoName(args)
py2: super(subclass, instance).methoName(args)

Py2:
class MyParentClass():
    def __init__(self, x, y):
       pass

class SubClass(MyParentClass):
    def __init__(self, x, y):
       super(SubClass, self).__init__(x, y)

Py3:
class MyParentClass():
    def __init__(self, x, y):
       pass

class SubClass(MyParentClass):
    def __init__(self, x, y):
       super().__init__(x, y)

8.Python 3.x:
class MyClass(object): = new-style class
class MyClass: = new-style class (implicitly inherits from object)

Python 2.x:
class MyClass(object): = new-style class
class MyClass: = OLD-STYLE CLASS

"""

# Py2
print 7/5  # 1  Performs the integer division

# Py3
print 7/5  # 1.4

# so use the floating point value to make it work with py3
print 7.0/5 # 1.4
print 7/5.0 # 1.4


"""
Python 2 stores strings as ASCII by default
Python 3 stores strings as Unicode by default, whereas Python 2 requires you to mark
a string with a u if you want to store it as Unicode.
Unicode strings are more versatile than ASCII strings, they can store letters from foreign languages
as well as emoji and the standard Roman letters and numerals.
You can still label your Unicode strings with a u if you want to make sure your Python 3 code is compatible with Python 2.
"""
#Py2, Bytes and str are same
print type('abc')  # <type 'str'>
print type(b'abc') # <type 'str'>

#Py3 Bytes and str are different
print type('abc')  # <class 'str'>
print type('abc')  # <class 'bytes'>

#Py2 unicide and str are different
print(type('default string '))  # <type 'str'>
print(type(u'string with b '))  # <type 'unicode'>

#Py3 unicide and str are same
print type('abc')  # <class 'str'>
print type(u'abc')  # <class 'str'>

# Py2
l = xrange(5) # Return iterator object
# Py3, xrange not exists

# Py2, slicing does not work
# print l[2:3] # Error
print l[2]


# Py2, Returns list
l = range(10) # [0,1,2,3,4,5,6,7,8,90
# Py3, return iterator object, but slicing works
l= range(10) # range(0, 10)
print l[1:4] # range(1,4)
print l[0] # 0


print 7/5 # 1
# from __future__ import division  # SyntaxError: from __future__ imports must occur at the beginning of the file
print 7/5 # 1.4

# from __future__ import print_function
print(10)

a=3
l = [a for a in [1,2,3]]
print l
print a


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