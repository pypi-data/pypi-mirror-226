"""
Move all negative elements to end in order with extra space allowed
Given an unsorted array of both negative and positive integer. The task is place all
negative element at the end of array without changing the order of positive element and negative element.

Examples:

Input : arr[] = {1, -1, 3, 2, -7, -5, 11, 6 }
Output : 1  3  2  11  6  -1  -7  -5

Input : arr[] = {-5, 7, -3, -4, 9, 10, -1, 11}
Output : 7  9  10  11  -5  -3  -4  -1
"""


import copy


# Following approach does not maintain order
def move_negative_to_end(arr):
    temp_arr = copy.copy(arr)

    li = 0
    ri = len(arr) - 1

    for a in temp_arr:
        if a < 0:
            arr[ri] = a
            ri -= 1
        else:
            arr[li] = a
            li += 1


# Following approach does not maintain order
def move_negative_to_end2(arr):
    li = 0
    ri = len(arr) - 1
    while li < ri:
        if arr[li] < 0:
            arr[li], arr[ri] = arr[ri], arr[li]
            ri -= 1
        else:
            li += 1


# Maintains order
def segregateElements(arr):
    n = len(arr)
    # Create an empty array to store result
    temp = [0 for k in range(n)]

    # Traversal array and store +ve element in
    # temp array
    j = 0  # index of temp
    for i in range(n):
        if (arr[i] >= 0):
            temp[j] = arr[i]
            j += 1

    # If array contains all positive or all negative.
    if (j == n or j == 0):
        return

    # Store -ve element in temp array
    for i in range(n):
        if (arr[i] < 0):
            temp[j] = arr[i]
            j += 1

    # Copy contents of temp[] to arr[]
    for k in range(n):
        arr[k] = temp[k]

"""
Time Complexity : O(n)
Auxiliary space : O(n)

What is the complexity of two "adjacent" loops? It is O(n) + O(n). 
Or you could think of this as O(n + n) --> O(2n). 
Constants drop out of complexity, so this is O(n).
"""

if __name__ == '__main__':
    l = [1, -1, 3, 2, -7, -5, 11, 6]
    move_negative_to_end(l)
    print l # [1, 3, 2, 11, 6, -5, -7, -1]

    l = [1, -1, 3, 2, -7, -5, 11, 6]
    move_negative_to_end2(l) # [1, 6, 3, 2, 11, -5, -7, -1]
    print l

    l = [1, -1, 3, 2, -7, -5, 11, 6]
    segregateElements(l)
    print l  # [1, 3, 2, 11, 6, -1, -7, -5]