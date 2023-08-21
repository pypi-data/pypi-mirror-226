"""
Given an array A[] and a number x, check for pair in A[] with sum as x
Write a program that, given an array A[] of n numbers and another number x,
determines whether or not there exist two elements in S whose sum is exactly x.

hasArrayTwoCandidates (A[], ar_size, sum)
1) Sort the array in non-decreasing order.
2) Initialize two index variables to find the candidate
   elements in the sorted array.
       (a) Initialize first to the leftmost index: l = 0
       (b) Initialize second  the rightmost index:  r = ar_size-1
3) Loop while l < r.
       (a) If (A[l] + A[r] == sum)  then return 1
       (b) Else if( A[l] + A[r] <  sum )  then l++
       (c) Else r--
4) No candidates in whole array - return 0
"""


def find_pair(arr, item):
    for i in range(len(arr)-1):
        for j in range(len(arr)):
            if arr[i] + arr[j] == item:
                return arr[i], arr[j]


def hasArrayTwoCandidates(A,  item):
    # sort the array
    A.sort()
    print A
    arr_size = len(A)
    l = 0
    r = arr_size - 1

    # traverse the array for the two elements
    while l < r:
        #print A[l], A[r]
        if A[l] + A[r] == item:
            print A[l], A[r]
            l += 1
            r -= 1

        elif  A[l] + A[r] < item:
            l += 1 # if item is grater than the pairs, It means move to next bigger number
        else:
            r -= 1


def printPairs(arr, sum):
    # Create an empty hash set
    arr_size = len(arr)
    s = set()
    for i in range(0, arr_size):
        temp = sum - arr[i]
        if temp >= 0 and temp in s:
            return arr[i], temp
        s.add(arr[i])

# This method works in O(n) time.
# Auxiliary Space: O(n) where n is size of array.

if __name__ == '__main__':
    a = [1, 4, 45, 6, 10, -8]
    x = 16
    print find_pair(a, x)
    print '..........................'
    a = [1, 4, 45, 6, 10, -8]
    x = 16
    print printPairs(a, x)
    print '..........................'

    a = [1, 4, 45, 6, 10, -8, 12]
    x = 16
    print hasArrayTwoCandidates(a, x)