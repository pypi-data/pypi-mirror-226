"""
Find a peak element
Given an array of integers. Find a peak element in it. An array element is peak
if it is NOT smaller than its neighbors. For corner elements,
 we need to consider only one neighbor.
For example, for input array {5, 10, 20, 15}, 20 is the only peak element.
For input array {10, 20, 15, 2, 23, 90, 67}, there are two peak elements: 20 and 90.
 Note that we need to return any one peak element.

Following corner cases give better idea about the problem.
1) If input array is sorted in strictly increasing order, the last element is always a peak element. For example, 50 is peak element in {10, 20, 30, 40, 50}.
2) If input array is sorted in strictly decreasing order, the first element is always a peak element. 100 is the peak element in {100, 80, 60, 50, 20}.
3) If all elements of input array are same, every element is a peak element.

"""
def find_peak_element(arr):

    for i in range(len(arr)):

        if i == 0:
            if arr[i] > arr[i+1]:
                print "Peak element is ", arr[i]
        elif i == len(arr)-1:
            if arr[i] > arr[i-1]:
                print "Peak element is ", arr[i]
        else:
            if arr[i] > arr[i-1] and arr[i] > arr[i+1]:
                print "Peak element is ", arr[i]


if __name__ == '__main__':
    a1 = [5, 10, 20, 15]
    find_peak_element(a1) # 20
    print '......................'
    a2 = [10, 20, 15, 2, 23, 90, 67]
    find_peak_element(a2) # 20, 90
    print '.....................'
    a3 = [0, 20, 30, 40, 50]
    find_peak_element(a3)  # 50
    print '...............'
    a4 = [100, 80, 60, 50, 20]
    find_peak_element(a4)  # 100