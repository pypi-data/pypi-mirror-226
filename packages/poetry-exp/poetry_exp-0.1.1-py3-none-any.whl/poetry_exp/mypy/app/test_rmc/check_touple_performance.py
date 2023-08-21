"""The dis module disassembles the byte code for a function and is useful to see the difference between tuples and lists.

In this case, you can see that accessing an element generates identical code, but that assigning a tuple is much faster than assigning a list.

>>> def a():
...     x=[1,2,3,4,5]
...     y=x[2]
...
>>> def b():
...     x=(1,2,3,4,5)
...     y=x[2]
...
>>> import dis

>>> dis.dis(a)
  2           0 LOAD_CONST               1 (1)
              3 LOAD_CONST               2 (2)
              6 LOAD_CONST               3 (3)
              9 LOAD_CONST               4 (4)
             12 LOAD_CONST               5 (5)
             15 BUILD_LIST               5
             18 STORE_FAST               0 (x)

  3          21 LOAD_FAST                0 (x)
             24 LOAD_CONST               2 (2)
             27 BINARY_SUBSCR
             28 STORE_FAST               1 (y)
             31 LOAD_CONST               0 (None)
             34 RETURN_VALUE
>>> dis.dis(b)
  2           0 LOAD_CONST               6 ((1, 2, 3, 4, 5))
              3 STORE_FAST               0 (x)

  3           6 LOAD_FAST                0 (x)
              9 LOAD_CONST               2 (2)
             12 BINARY_SUBSCR
             13 STORE_FAST               1 (y)
             16 LOAD_CONST               0 (None)
             19 RETURN_VALUE
"""