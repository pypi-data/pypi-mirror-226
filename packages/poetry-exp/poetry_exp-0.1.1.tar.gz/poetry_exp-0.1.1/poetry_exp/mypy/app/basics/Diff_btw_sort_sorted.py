
"""

list.sort() when you want to in-place sort of items of the list,
sorted() when you want a new sorted object. It Can be use for touple which cannot be modified
For lists, list.sort() is faster than sorted() because it doesn't have to create a copy.
"""


class Emp(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self): # list will use this  not __str__
        return self.name


if __name__ == '__main__':
    l1 = [9,3,4,2,8,1]
    l1.sort()  # in place sort

    t1 = (4,3,6,1,9)
    # t1.sort() This method does not work for touple

    d1 = {"B":2, "a":1, "C":3}
    # d1.sort() This method does not work for dict

    # "bdac".sort() This method does not work for str

    set1 = {5,2,1,7,9}
    #set1.sort() # This method does not work for set

    # User defined object
    e1 = Emp("b")
    e2 = Emp("a")
    e3 = Emp("c")
    emp_list = [e1,e2,e3]
    emp_list.sort()
    print emp_list # [b, a, C], no sorting happen
    emp_list.sort(key=lambda e:e.name)
    print emp_list  # [a, b, c]

    # sorted, always returns the new sorted list of items in sequence/iterable
    l1 = [9, 3, 4, 2, 8, 1]
    l2 = sorted(l1)  # returns new list
    print l1  # [9, 3, 4, 2, 8, 1]
    print l2  # [1, 2, 3, 4, 8, 9]

    t2 = sorted(t1) # accept touple but returns list
    print t1  # (4, 3, 6, 1, 9)
    print t2  # [1, 3, 4, 6, 9]

    d2 = sorted(d1) # accept dict, returns list of sorted keys
    print d1  # {'a': 1, 'C': 3, 'B': 2}
    print d2  # ['B', 'C', 'a'] # By default sort keys in descending order

    d2 = sorted(d1, reverse=True) # accept dict, returns list of sorted keys
    print d1  # {'a': 1, 'C': 3, 'B': 2}
    print d2  # ['a', 'C', 'B']

    s1 = "badc"
    s2 = sorted(s1)  # accept string, but returns list of sorted chars of string
    print s1  # badc
    print s2 # ['a', 'b', 'c', 'd']

    set2 = sorted(set1)
    print set1 # set([1, 2, 9, 5, 7])
    print set2 # [1, 2, 5, 7, 9]

    # user defined object
    emp_list = [e1, e2, e3]
    emp_list2 = sorted(emp_list)
    print emp_list2  # [b, a, C], no sorting happen
    emp_list2 = sorted(emp_list, key=lambda o:o.name)
    print emp_list2  # [a, b, c]


"""
[a, c, b]
[a, b, c]
[9, 3, 4, 2, 8, 1]
[1, 2, 3, 4, 8, 9]
(4, 3, 6, 1, 9)
[1, 3, 4, 6, 9]
{'a': 1, 'C': 3, 'B': 2}
['B', 'C', 'a']
{'a': 1, 'C': 3, 'B': 2}
['a', 'C', 'B']
badc
['a', 'b', 'c', 'd']
set([1, 2, 9, 5, 7])
[1, 2, 5, 7, 9]
[a, c, b]
[a, b, c]


"""