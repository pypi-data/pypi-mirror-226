"""
Segregate even and odd numbers | Set 3
Given an array of integers, segregate even and odd numbers in the array. All the even numbers should be present first, and then the odd numbers.

Examples:

Input : 1 9 5 3 2 6 7 11
Output : 2 6 5 3 1 9 7 11

Input : 1 3 2 4 7 6 9 10
Output : 2 4 6 10 7 1 9 3

"""


import copy


def segregate_even_odd(arr):
    li = 0
    ri = len(arr) - 1
    temp_array = copy.copy(arr)
    for a in temp_array:
        if a % 2 == 1:
            arr[ri] = a
            ri -= 1
        else:
            arr[li] = a
            li += 1


def segregate_even_odd2(arr):
    li = 0
    ri = len(arr) - 1
    # Traverse the array and if odd number is encountered then swap it with the first even element.
    while li < ri:
        if arr[li] % 2 == 1:
            arr[li], arr[ri] = arr[ri], arr[li]
            ri -= 1
        else:
            li += 1

"""
Time Complexity : O(n)
Auxiliary Space : O(1)
"""


if __name__ == '__main__':
    l = [1, 9, 5, 3, 2, 6, 7, 11]
    segregate_even_odd(l)
    print l

    l = [1, 9, 5, 3, 2, 6, 7, 11]
    segregate_even_odd2(l)
    print l

    l = [1, 3, 2, 4, 7, 6, 9, 10]
    segregate_even_odd(l)
    print l

    l = [1, 3, 2, 4, 7, 6, 9, 10]
    segregate_even_odd2(l)
    print l