"""
Generators are iterators, but you can only iterate over them once. Its because they do
not store all the values in memory, they generate the values on the fly. You use them
by iterating over them, either with a for loop or by passing them to any function
or construct that iterates. Most of the time generators are implemented as functions.
However, they do not return a value, they yield it.
They are also similar to list comprehensions. The only difference is that they dont
allocate memory for the whole list but generate one item at a time, thus more memory
effecient.

Generators are best for calculating large sets of
results (particularly calculations involving loops themselves) where you dont want to
allocate the memory for all results at the same time. Many Standard Library functions
that return lists in Python 2 have been modified to return generators in Python 3
because generators require fewer resources.
"""

numbers = range(20)
odd_numbers = (n for n in numbers if n%2==1)
print odd_numbers # <generator object <genexpr> at 0x000000000270D2D0>

for num in odd_numbers:
    print num

"""
1
3
5
7
9
11
13
15
17
19
"""