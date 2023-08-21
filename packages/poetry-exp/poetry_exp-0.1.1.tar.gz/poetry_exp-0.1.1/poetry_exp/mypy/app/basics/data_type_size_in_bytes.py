"""

>>> import sys
>>> sys.getsizeof(10)   # Integer
24
>>> sys.getsizeof(10.5) # Float
24
>>> sys.getsizeof(long())
24
>>> sys.getsizeof(long(1))
28
>>>
>>> sys.getsizeof("") # String
33
>>> sys.getsizeof("a") # Each char add 1 bytes
34
>>> sys.getsizeof([]) # List
64
>>> sys.getsizeof([1]) # Each element add 8 bytes
72
>>> sys.getsizeof(())
48
>>> sys.getsizeof((10))
24
>>> sys.getsizeof({})
272
>>> sys.getsizeof({"a":1})
272
>>> sys.getsizeof({"a":1, "b":2})
272
>>>
>>> sys.getsizeof({1})
224
>>> sys.getsizeof(set())
224
>>> sys.getsizeof(list())
64
>>> sys.getsizeof(set([]))
224
>>> sys.getsizeof(set([3]))
224
>>> sys.getsizeof(set([3,4]))
224
>>> sys.getsizeof(set([3,4]))

"""