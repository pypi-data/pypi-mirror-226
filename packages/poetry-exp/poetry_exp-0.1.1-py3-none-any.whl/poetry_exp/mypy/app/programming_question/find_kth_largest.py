
def find_kth_largest(arr, k):
    arr.sort(reverse=True)
    # print arr
    return arr[k-1]


def find_kth_smallest(arr, k):
    arr.sort()
    # print arr
    return arr[k-1]


"""
ASSUMPTION: ALL ELEMENTS IN ARR[] ARE DISTINCT, means Array should not have duplicate number
"""


if __name__ == '__main__':
    a = [2, 5, 7, 1, 9, 6]  # after sort [9, 7, 6, 5, 2, 1]
    print find_kth_largest(a, 2)  # 7

    a2 = [2, 5, 7, 1, 9, 6]  # after sort [1, 2, 5, 6, 7, 9]
    print find_kth_smallest(a2, 2)  # 2

    print find_kth_largest(a, 4)  # 5
    print find_kth_smallest(a2, 4)  # 6
