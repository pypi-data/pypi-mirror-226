"""
Enumerate is a built-in function of Python, It allows us to loop over something and have an automatic counter

"""


def square_list_in_place(arr):
    for i, a in enumerate(arr):
        arr[i] = a**2  # a^3 = a**3


def remove_duplicates_in_place(arr):
    for i, a in enumerate(arr):
        if arr.count(a)>1:
            del arr[i]


a = [1, 2, 3, 1, 3, 4, 6, 1]
remove_duplicates_in_place(a)
print a # [2, 1, 3, 4, 6]

a = [1, 2, 3]
square_list_in_place(a)
print a # [1, 4, 9]

for counter, value in enumerate(['Red', 'Green', 'Blue']):
    print counter, value
"""
0 Red
1 Green
2 Blue
"""

"""
enumerate also accepts an optional argument which tell enumrate to start the index number
"""

for counter, value in enumerate(['Red', 'Green', 'Blue'], 2):
    print counter, value

"""
2 Red
3 Green
4 Blue
"""

"""
You can also create tuples containing the index and list item using a list
"""

colours = list(enumerate(['Red', 'Green', 'Blue'], 1))
print colours  # [(1, 'Red'), (2, 'Green'), (3, 'Blue')]

