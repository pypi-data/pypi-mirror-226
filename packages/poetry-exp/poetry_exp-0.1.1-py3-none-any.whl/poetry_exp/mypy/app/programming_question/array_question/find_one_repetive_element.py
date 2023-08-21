"""
Find the only repetitive element between 1 to n-1
We are given an array arr[] of size n. Numbers are from 1 to (n-1) in random order.
 The array has only one repetitive element. We need to find the repetitive element.

Examples :

Input  : a[] = {1, 3, 2, 3, 4}
Output : 3

Input  : a[] = {1, 5, 1, 2, 3, 4}
Output : 1
"""


def find_repetitive_element(arr):
    n = len(arr) - 1  # since one element repetitive
    expected_sum = n * (n+1)/2.0
    actual_sum = sum(arr)
    return int(actual_sum - expected_sum)


if __name__ == '__main__':
    a1 = [1, 3, 2, 3, 4]
    print find_repetitive_element(a1)  # 3

    a2 = [1, 5, 1, 2, 3, 4]
    print find_repetitive_element(a2)  # 1
