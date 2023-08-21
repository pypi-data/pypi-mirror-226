"""
Reduce is a really useful function for performing some computation on a list and returning
the result. It applies a rolling computation to sequential pairs of values in a
list. For example, if you wanted to compute the product of a list of integers
"""

# product of list of integer

from functools import reduce
int_list = [1,2,3,4, 5]
p = reduce(lambda x, y: x*y, int_list)
print p


"""

>>> l1
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> l2
[10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
>>> map((lambda x, y: x*y),  l1, l2)
[0, 11, 24, 39, 56, 75, 96, 119, 144, 171]
>>> reduce((lambda x, y: x*y),  l1, l2)
[]
>>> filter((lambda x, y: x*y),  l1, l2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: filter expected 2 arguments, got 3
"""