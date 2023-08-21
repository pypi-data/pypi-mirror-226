"""
Ordered Collections of Data: List, Touple, Set
UnOrdered Collections of Data: Dict

Ordered means: Stored in the same order in which they inserted, so while traverse you will get it in same order

Mutable: List, Set, Dict
Immutable: Touple, String, frozenset

Time complexity:
Set: O(1) on average.(uses hash table since looking up an item in a hashtable is an O(1) operation, on average.)
     does not allow duplicates. For each item a hash is calculated and keep that value, if same hash for different
     value then its get stored to next element in linked list, during look up again hash calculated and then compare the
     value in linked list ( knid of array of linked list)
dict: O(1)



list: Like array in other language, but flexible to store different type element
The costly operation is inserting or deleting the element from the beginning of the List
as all the elements are needed to be shifted.

Insertion and deletion at the end of the list can also become costly in the case where
the preallocated memory becomes full.

touple: like a list but Tuples are immutable in nature i.e. the elements in the tuple cannot be
 added or removed once created. Just like a List, a Tuple can also contain elements of various types.
>>> t=2,
>>> type(t)
<class 'tuple'>
>>> t1=(1,'a',[1,2])
>>> type(t1)
<class 'tuple'>
>>> t3=(1,)
>>> type(t1)
<class 'tuple'>
>>> type(t3)
<class 'tuple'>
>>>
>>> t3[0]=3
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>>

dict: like hash table with the time complexity O(1), stores key value pairs, values can be anything(any data type)
Indexing of dict is done with the help of keys. Keys can be any hashable type i.e.(strings, number, touple)
 an object whose can  never change
>>> d={}
>>> type(d)
<class 'dict'>
>>> t1=(1,[1,2,3],{'a':1})
>>> t1
(1, [1, 2, 3], {'a': 1})
>>> t1[1].append(4) # allows because list memory reference gets stored not the list
>>> t1
(1, [1, 2, 3, 4], {'a': 1})
>>> id(t1[1])
93255000
>>> t1[1].append(5)
>>> id(t1[1])
93255000  # no change in memory refrence
>>>


set:  an ordered collection of data(hashable(string, numbers)) that is mutable and does not allow any duplicate element.
Sets are basically used to include membership testing and eliminating duplicate entries.
The data structure used in this is Hashing, a popular technique to perform insertion, deletion,
 and traversal in O(1) on average.

If Multiple values are present at the same index position, then the value is appended to that
index position, to form a Linked List.
In, CPython Sets are implemented using a dictionary with dummy variables, where key beings
the members set with greater optimizations to the time complexity.

>>> s1=set(1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'int' object is not iterable
>>> s1=set()
>>> s1.add(1)
>>> s1
{1}
>>> s1=set([1, 2, 'Geeks', 4, 'For', 6, 'Geeks'])
>>> s1
{1, 2, 4, 6, 'Geeks', 'For'}

>>> s1.add(1)
>>> print(s1.add(1))
None
>>> print(s1.add(3))
None
>>> s1
{1, 2, 3, 4, 6, 'Geeks', 'For'}
>>>
>>> s1.add([1,2])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
>>>

>>> s1[1]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'set' object does not support indexing
>>>

>>> s1.remove('For')
>>> s1
{1, 2, 3, 4, 6, 'Geeks'}
>>>
>>>


frozenset: Immutable objects, elements of the frozen set remain the same after creation.
>>> fs=frozenset([1, 2, 'Geeks', 4, 'For', 6, 'Geeks', 1, 'For'])
>>> fs
frozenset({1, 2, 4, 6, 'Geeks', 'For'})
>>>
>>> fs.add(3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'frozenset' object has no attribute 'add'
>>> fs.remove(3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'frozenset' object has no attribute 'remove'



str: arrays of bytes representing Unicode characters. In simpler terms, a string is an immutable array of characters.
Python does not have a character data type, a single character is simply a string with a length of 1.

Note: As strings are immutable, modifying a string will result in creating a new copy.



bytearray: gives a mutable sequence of integers in the range 0 <= x < 256.

>>> ba=bytearray((1,2,3,4))
>>> ba
bytearray(b'\x01\x02\x03\x04')
>>> ba=bytearray([1,2,3,4])
>>> ba
bytearray(b'\x01\x02\x03\x04')

>>> ba=bytearray([1,2,3,4])
>>> ba[0]=10
>>> ba
bytearray(b'\n\x02\x03\x04')
>>> ba[1]=11
>>> ba[2]=12
>>> ba
bytearray(b'\n\x0b\x0c\x04')
>>>
"""