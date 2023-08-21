"""
Print n smallest elements from given array in their original order
We are given an array of m-elements, we need to find n smallest elements from the array
but they must be in the same order as they are in given array.

Input : arr[] = {4, 2, 6, 1, 5},
        n = 3
Output : 4 2 1
Explanation :
1, 2 and 4 are 3 smallest numbers and
4 2 1 is their order in given array.

Input : arr[] = {4, 12, 16, 21, 25},
        n = 3
Output : 4 12 16
Explanation :
4, 12 and 16 are 3 smallest numbers and
4 12 16 is their order in given array.

Approach:
 Make a copy of original array and then sort copy array. After sorting the copy array,
  save all n smallest numbers. Further for each element in original array,
   check whether it is in n-smallest number or not if it present in n-smallest array then print it otherwise move forward.
"""

import copy


def find_n_smallest_in_order(arr, n):
    temp_copy = copy.copy(arr) # Take extra space o(n)
    arr.sort() # o(nlog n)
    n_smallest = arr[0:n]
    n_smallest_in_order = []
    for a in temp_copy:
        if a in n_smallest:
            n_smallest_in_order.append(a)
    return n_smallest_in_order


if __name__ == '__main__':
    a = [4, 12, 16, 21, 25]
    print find_n_smallest_in_order(a, 3)


"""
For making a copy of array we need space complexity of O(n) and then for sorting
we will need complexity of order O(n log n). Further for each element in arr[] we
are performing searching in copy_arr[], which will result O(n) for linear search but
 we can improve it by applying binary search and hence our overall time complexity will be O(n log n).
"""
