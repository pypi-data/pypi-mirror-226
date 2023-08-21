"""
Find all distinct pairs with difference equal to k
Given an integer array and a positive integer k, FInd all distinct pairs with difference equal to k.

Examples:

Input: arr[] = {1, 5, 3, 4, 2}, k = 3
Output: 2
There are 2 pairs with difference 3, the pairs are {1, 4} and {5, 2}

Input: arr[] = {8, 12, 16, 4, 0, 20}, k = 4
Output: 5
There are 5 pairs with difference 4, the pairs are {0, 4}, {4, 8},
{8, 12}, {12, 16} and {16, 20}

"""


def find_pairs_with_diff_k(arr, k):
    arr.sort()
    print arr
    l = 0
    r = 0
    size = len(arr)
    while r < size:
        print 'L: ', l
        print 'R:', r
        if arr[r] - arr[l] == k:
            print (arr[l], arr[r])
            l += 1
            r += 1
        elif arr[r] - arr[l] > k:
            l += 1
        else:
            r += 1


if __name__ == '__main__':
    a = [1, 5, 3, 4, 2]
    k = 3
    find_pairs_with_diff_k(a, k)
    print '...............'
    a = [8, 12, 16, 4, 0, 20]
    k = 4
    find_pairs_with_diff_k(a, k)

"""
[1, 2, 3, 4, 5]
(1, 4)
(2, 5)
...............
[0, 4, 8, 12, 16, 20]
(0, 4)
(4, 8)
(8, 12)
(12, 16)
(16, 20)

"""