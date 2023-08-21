import math

# Interchange first and last element
l = [1, 2, 2, 3, 4]
l[0], l[-1] = l[-1], l[0]
print(l)  # [4, 2, 2, 3, 1]


def swapList(list):
    first = list.pop(0)
    last = list.pop(-1)

    list.insert(0, last)
    list.append(first)

    return list


# check-if-element-exists-in-list-in-python
print(3 in l)  # True
print(l.count(3) > 0)  # True
# Efficient way
print(3 in set(l))  # True
print(l)  # [4, 2, 2, 3, 1]

"""
But having efficiency for a plus also has certain negatives.
One among them is that the order of list is not preserved, and if you opt to take a new list for it,
you would require to use extra space. Another drawback is that set disallows duplicity and hence duplicate
elements would be removed from the original list.
"""


# sum of all element of list
print(sum(l))  # 12

# find smallest
print(min(l))  # 1
l.sort()  # in place sort
print(l[0])  # 1