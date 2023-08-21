"""
A linked list is an ordered collection of values. Linked lists are similar to arrays in the sense that
they contain objects in a linear order. However they differ from arrays in their memory layout

Arrays are contiguous data structures and they are composed of fixed-size data records stored in
adjoining blocks of memory. In an array, data is tightly packed and we know the size of each
data record which allows us to quickly look up an element given its index in the array


Linked lists, however, are made up of data records linked together by pointers.
This means that the data records that hold the actual data payload can be stored anywhere in memory
what creates the linear ordering is how each data record points to the next one

There are two different kinds of linked lists: singly-linked lists and doubly-linked lists.
 What you saw in the previous example was a singly-linked list each element in it has a reference to (a pointer)
  to the next element in the list.
In a doubly-linked list, each element has a reference to both the next and the previous element.
Why is this useful? Having a reference to the previous element can speed up some operations, like removing (unlinking)
an element from a list or traversing the list in reverse order.

Insertion and removal are faster(o(1)) where as search is expensive (0(n))
"""

# Use deque as link list
import collections
from collections import deque

lst = deque()

# Inserting elements at the front or back takes O(1) time:
lst.append('B')
lst.append('C')

lst.appendleft('A')

print lst  # deque(['A', 'B', 'C'])

print dir(lst) # 'append', 'appendleft', 'clear', 'count', 'extend', 'extendleft', 'maxlen', 'pop', 'popleft', 'remove', 'reverse', 'rotate'
# However, inserting elements at arbitrary indexes takes O(n) time:
# lst.insert(2, 'X')
# print lst


# Removing elements at arbitrary # indexes or by key takes O(n) time again:
del lst [1]
lst.remove('C')
print lst  # deque(['A'])

# Deques can be reversed in-place
lst = collections.deque(['A', 'B', 'X', 'C'])
lst.reverse()
print lst # deque(['C', 'X', 'B', 'A'])


# Searching for elements takes  O(n) time:
print lst.index('X')



