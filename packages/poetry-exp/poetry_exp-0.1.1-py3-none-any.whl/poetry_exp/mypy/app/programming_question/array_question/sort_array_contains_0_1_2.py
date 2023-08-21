"""
Sort an array of 0s, 1s and 2s (Simple Counting)
Given an array A[] consisting 0s, 1s and 2s, write a function that sorts A[].
The functions should put all 0s first, then all 1s and all 2s in last.

Input :  {0, 1, 2, 0, 1, 2}
Output : {0, 0, 1, 1, 2, 2}

Input :  {0, 1, 1, 0, 1, 2, 1, 2, 0, 0, 0, 1}
Output : {0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2}

Approach1:
Count the number of 0s, 1s and 2s. After Counting, put all 0s first,
then 1s and lastly 2s in the array.
We traverse the array two times. Time complexity will be O(n).

Approach2:
https://www.geeksforgeeks.org/sort-an-array-of-0s-1s-and-2s/

The problem was posed with three colours, here 0, 1 and 2. The array is divided into four sections:

a[1..Lo-1] zeroes (red)
a[Lo..Mid-1] ones (white)
a[Mid..Hi] unknown
a[Hi+1..N] twos (blue)
"""


def sort_arr(arr):
    count0 = 0
    count1 = 0
    count2 = 0

    for a in arr:
        if a == 0:
            count0 += 1
        elif a == 1:
            count1 += 1
        else:
            count2 += 1

    for i in range(0, count0):
        arr[i] = 0

    for j in range(count0, count0+count1):
        arr[j] = 1

    for k in range(count0+count1, len(arr)):
        arr[k] = 2


def sort_arr2(arr):
    li = 0
    ri = len(arr) - 1
    mid = 0
    while mid <= ri:
        if arr[mid] == 0:
            arr[mid], arr[li] = arr[li], arr[mid]
            li += 1
            mid += 1
        elif arr[mid] == 1:
            mid += 1
        else:
            arr[mid], arr[ri] = arr[ri], arr[mid]
            ri -= 1


if __name__ == '__main__':
   l = [0, 1, 2, 0, 1, 2]
   sort_arr(l)
   print l
   l2 = [0, 1, 1, 0, 1, 2, 1, 2, 0, 0, 0, 1]
   sort_arr(l2)
   print l2

   l3 = [0, 1, 2, 0, 1, 2]
   sort_arr2(l3)
   print l3
   l4 = [0, 1, 1, 0, 1, 2, 1, 2, 0, 0, 0, 1]
   sort_arr2(l4)
   print l4
