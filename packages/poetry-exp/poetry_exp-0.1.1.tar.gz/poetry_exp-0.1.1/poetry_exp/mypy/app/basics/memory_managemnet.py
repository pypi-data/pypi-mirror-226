"""
>>> x = 8
>>> y = x
>>> x = 100
>>> y
8

>>> L = [1, 2, 3]
>>> type(L)
<class 'list'>
another built-in function isinstance() also checks if an object belongs to a given class by returning a boolean value.
The difference is that isinstance() checks subclasses in addition, while type() doesnt.

>>> a=10
>>> type(a)
<type 'int'>
>>> isinstance(a, int)
True
>>>

>>> class A(object):
...    pass
...
>>> class B(A):
...   pass
...
>>> b=B()
>>> isinstance(b, A)  # check for subclass
True
>>>


>>> type(b)
<class '__main__.B'>
>>>


There are two kinds of objects in Python: Mutable objects and Immutable objects.
The value of a mutable object can be modified in place after its creation,
while the value of an immutable object cannot be changed.

Immutable Object: int, float, long, complex, string tuple, bool
Mutable Object: list, dict, set, byte array, user-defined classes

check the mutability of an object by attempting to modify it and see if it is
still the same object. There are two ways to do this:

Using the built-in function id():
   this function returns the unique identity of an object.
   In CPython implementation, id() returns the memory address of the object. No two objects have the same identity.
Using the is and is not operator:
    these identity operators evaluates whether or not the objects have the same identity.
     In other words, if they are the same object.

>>> a = 89
>>> id(a)
4434330504
>>> a = 89 + 1  # modify a
>>> print(a)
90
>>> id(a)
4430689552  # this is different from before!


>>> L = [1, 2, 3]
>>> id(L)
4430688016
>>> L += [4]  # Modify
>>> print(L)
[1, 2, 3, 4]
>>> id(L)
4430688016    # this is the same as before!


variables in Python refer to values (or objects) stored somewhere in memory.
In fact, all variable names in Python are said to be references to the values,
some of which are front loaded by Python and therefore exist before the name references occur (more on this later).

Python keeps an internal counter on how many references an object has. Once the counter goes to zero
meaning that no reference is made to the object
the garbage collector in Python removes the object , thus freeing up the memory.


>>> L1 = [1, 2, 3]
>>> L2 = [1, 2, 3]
>>> L1 == L2
True             # L1 and L2 have the same value
>>> L1 is L2
False            # L1 and L2 do not refer to the same object

We can, however, have two variables refer to the same object through a process called aliasing:
assigning one variable the value of the other variable.
>>> L1 = [1, 2, 3]
>>> L2 = L1         # L2 now refers to the same object as L1
>>> L1 == L2
True
>>> L1 is L2
True
>>> L1.append(4)
>>> print(L2)
[1, 2, 3, 4]

Since L1 and L2 both refer to the same object, modifying L1 results in the same change in L2.


Exceptions with Immutable Objects
While it is true that a new object is created each time we have a variable that makes reference to it,
there are few notable exceptions:

  - some strings
  - Integers between -5 and 256 (inclusive)
  - empty immutable containers (e.g. tuples)
These exceptions arise as a result of memory optimization in Python implementation.
After all, if two variables refer to objects with the same value, why wasting memory creating a new object
for the second variable? Why not simply have the second variable refer to the same object in memory


String Interning:
>>> a = "python is cool!"
>>> b = "python is cool!"
>>> a is b
False
This should not be surprising, since it obeys the new objects are created each time rule.

>>> a = "python"
>>> b = "python"
>>> a is b
True   # a and b refer to the same object!

>>> a="python a"
>>> a="python a"
>>> a is b
False
>>>

>>> b = "p a"
>>> c="p a"
>>> b is c
False
>>>
This is a result of string interning, which allows two variables to refer to the same string object.
Python automatically does this, although the exact rules remain fuzzy.



Integer Caching

The Python implementation front loads an array of integers between -5 to 256. Hence, variables referring to an integer within the range would be pointing to the same object that already exists in memory:

>>> a = 256
>>> b = 256
>>> a is b
True
This is not the case if the object referred to is outside the range:

>>> a = 257
>>> b = 257
>>> a is b
False

Empty Immutable Objects

Lets take a look at empty tuples, which are immutable:

>>> a = ()
>>> b = ()
>>> a is b
True  # a and b both refer to the same object in memory


The Tricky Case with Operators
We have seen in the earlier example that given a list L, we can modify it in place using L += [x], which is equivalent to L.append(x). But how about L = L + [x] ?

>>> L = [1, 2, 3]
>>> id(L)
4431388424
>>> L = L + [4]
>>> id(L)
4434330504     # L now refers to a different object from before!
"""