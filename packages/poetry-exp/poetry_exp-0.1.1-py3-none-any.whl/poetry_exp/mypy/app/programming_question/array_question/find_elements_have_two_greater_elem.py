"""
Find all elements in array which have at-least two greater elements
Given an array of n distinct elements, the task is to find all elements in array which have
at-least two greater elements than themselves.

Input : arr[] = {2, 8, 7, 1, 5};
Output : 2  1  5
The output three elements have two or
more greater elements

Input  : arr[] = {7, -2, 3, 4, 9, -1};
Output : -2  3  4 -1


Approach1:
  Use two loops, for each elements finds all elements greater than this in second loop
  o(n2)

Approach2:
  sort the array first in increasing order, then we print first n-2 elements:  O(n Log n)

Approach3:
   first find second largest element and then find all emenets less tthan this

"""

def find_elements_have_two_greater_elements(arr):
    result = []
    for i in range(len(arr)):
        count = 0
        for j in range(len(arr)):
            if arr[j] > arr[i]:
                count += 1

        if count >=2:
            result.append(arr[i])

    return result


def find_elements_have_two_greater_elements2(arr):
    arr.sort()
    return arr[:-2]


def find_elements_have_two_greater_elements3(arr):
    result = []

    first = arr[0]
    second = arr[1]
    for i in range(len(arr)):
        if arr[i] > first:
            second = first
            first = arr[i]
        elif arr[i] > second:
            second = arr[i]

    for j in range(len(arr)):
        if arr[j] < second:
            result.append(arr[j])

    return result


if __name__ == '__main__':
    a = [2, 8, 7, 1, 5]
    print find_elements_have_two_greater_elements(a)

    a2 = [2, 8, 7, 1, 5]
    print find_elements_have_two_greater_elements2(a2)

    a3 = [2, 8, 7, 1, 5]
    print find_elements_have_two_greater_elements3(a3)