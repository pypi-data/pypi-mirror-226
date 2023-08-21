
"""
In Python, we have two objects that uses hash tables, dictionaries and sets:

A dictionary is a hash table and is called an associative array. In a dictionary,
 only keys are hashed and not the values. This is why a dictionary key should be an immutable object
  as well while values can be anything, even a list which is mutable.

A set contains unique objects which are hashable. If we have non-hashable items,
 we cannot use set and must instead use list.

>>> a= {a, {"a":1}}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: dict
>>>

>>> a= {a, []}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: list
>>>

"""


"""

Why dicts need immutable keys say you? Well, a dict is a hash table, and as such it stores a key in a location
 based on its value. 

For example, consider a parallel universe where my_dict, is a dictionary that allows mutable keys
 and that strings are mutable. Assume that currently the hash table of my_dict has 7 entries and it uses
  the hash function hash(k)%7. According to this,  k=hello is put in the 5-th entry of the hash table. No problem here,
   right?

Since in this parallel universe strings are mutable, it is possible to modify the key object from
 hello to bye. Now, out of the blue, our key in  my_dict has changed to bye,
  but it is still in its original 5-th place. Next, you query it with my_dict.has_key(bye), but that wont work.
   What? Why wont it work?!  This is because bye, in this example, maps to a the 3-ed location in my_dicts hash table,
    but it cannot be found there since it is still in the 5-th location of the hash table.

There are two different ways to avoid such problems.
1. Make strings immutable and require the keys to be immutable. This is what python does.
2. Deep-copy the keys before placing objects into dictionaries, 
this is kind of what c do.
 This goes against python philosophy of copying references rather than values.
  Never performing a deep-copy except here is surprising, and it is bad idea to surprise programmers.
"""

