"""
Given a sorted array arr[] of n elements, write a function to search a given element x in arr[].

A simple approach is to do linear search.The time complexity of above algorithm is O(n). Another approach to perform the same task is using Binary Search.

Binary Search: Search a sorted array by repeatedly dividing the search interval in half.
 Begin with an interval covering the whole array.
 If the value of the search key is less than the item in the middle of the interval,
  narrow the interval to the lower half. Otherwise narrow it to the upper half.
  Repeatedly check until the value is found or the interval is empty

The idea of binary search is to use the information that the array is sorted and reduce the time complexity to O(Log n).

1. Compare x with the middle element.
2. If x matches with middle element, we return the mid index.
3. Else If x is greater than the mid element, then x can only lie in right half subarray after the mid element. So we recur for right half.
Else (x is smaller) recur for the left half.

"""


# Python Program for recursive binary search.

# Returns index of x in arr if present, else -1
def binary_search(arr, left_index, right_index, item):
    if right_index < left_index:
        return -1

    mid = (left_index + right_index)/2
    if arr[mid] == item: # If element is present at the middle itself
        return mid
    elif arr[mid] > item: # If element is smaller than mid, then it can only be present in left subarray
        return binary_search(arr, left_index, mid-1, item)
    else:
        # If element is greater than mid, then it can only be present in right subarray
        return binary_search(arr, mid+1, right_index, item)

if __name__ == '__main__':
    a = [10, 20 ,30 ,40, 50, 60]
    print binary_search(a, 0, len(a)-1, 30)  # 2
    print binary_search(a, 0, len(a)-1, 90)  # -1
