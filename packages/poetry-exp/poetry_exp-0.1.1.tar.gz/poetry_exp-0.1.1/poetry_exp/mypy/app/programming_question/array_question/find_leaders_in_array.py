"""
Leaders in an array
Write a program to print all the LEADERS in the array. An element is leader if it is greater than all the elements to its right side.
 And the rightmost element is always a leader. For example int the array {16, 17, 4, 3, 5, 2}, leaders are 17, 5 and 2.

Let the input array be arr[] and size of the array be size.
Scan all the elements from right to left in array and keep track of maximum till now.
When maximum changes its value, print it.
"""

def find_leaders(arr):
    max_from_right = arr[len(arr) - 1]
    print 'leader is: ', max_from_right
    for i in range(len(arr)-2, 0, -1):
        if arr[i] > max_from_right:
            print 'leader is: ', arr[i]
            max_from_right = arr[i]

# Time complexity o(n)

if __name__ == '__main__':
    a = [16, 17, 4, 3, 5, 2]
    find_leaders(a)