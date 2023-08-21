"""
A ist is partitionnable if it can be divided into two list with equal sum

"""

from itertools import permutations


# Approach1:
def is_subset_exist_with_sum(arr, required_sum):
    for i in range(1, len(arr)+1):
        for perm in permutations(arr, i):
            if sum(perm) == required_sum:
                return True
    return False


def is_list_partitionable(arr):
    result = None
    size = len(arr)
    total_sum = sum(arr)
    # If sum is odd, then list cannot be partition
    if total_sum%2 == 1:
        result = False
    else:
        # Now try to find a list with half of total sum of list
        result = is_subset_exist_with_sum(arr, total_sum//2)

    print 'List: {0} is partitionable: {1}'.format(arr, result)
    return result


# Approach 2
def is_subset_exist_with_sum2(l, n, sum):
    # Base Cases
    if sum == 0:
        return True
    if n == 0 and sum != 0:
        return False

    # If last element is greater than sum, then
    # ignore it
    if l[n - 1] > sum:
        return is_subset_exist_with_sum2(l, n - 1, sum)

    ''' else, check if sum can be obtained by any of  
    the following 
    (a) including the last element 
    (b) excluding the last element'''

    return is_subset_exist_with_sum2(l, n - 1, sum) or is_subset_exist_with_sum2(l, n - 1, sum - l[n - 1])


def is_list_partitionable2(l):
    result = None
    size = len(l)
    total_sum = sum(l)
    if total_sum%2 == 1:
        result = False
    else:
       result = is_subset_exist_with_sum2(l, size-1, total_sum//2)
    print 'List: {0} is partitionable: {1}'.format(l, result)
    return result


if __name__ == '__main__':
    is_list_partitionable([])
    is_list_partitionable([3, 3])
    is_list_partitionable([3, 1])
    is_list_partitionable([1, 2, 3, 1, 2, 3])
    is_list_partitionable([1, 2, 3, 5, 1])
    is_list_partitionable([5, 1, 2, 3, 1])
    is_list_partitionable([6, 9, 3])
    is_list_partitionable([6, 9, 3, 1])



    # is_list_partitionable2([])
    # is_list_partitionable2([3,3])
    #
    # is_list_partitionable2([3, 1])
    # is_list_partitionable2([1,2,3,1,2,3])
    # is_list_partitionable2([1,2,3,5,1])
    # is_list_partitionable2([5,1,2,3,1])
    # is_list_partitionable2([6,9,3])
    # is_list_partitionable2([6, 9, 3, 1])