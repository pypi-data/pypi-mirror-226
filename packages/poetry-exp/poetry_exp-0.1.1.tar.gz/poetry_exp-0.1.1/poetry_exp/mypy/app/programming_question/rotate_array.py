
def left_rotate(arr):
    temp = arr[0]
    n = len(arr)
    for i in range(1, n):
        arr[i-1] = arr[i]

    arr[n-1] = temp


def right_rotate(arr):
    n = len(arr)
    temp = arr[n-1]
    for i in range(n-2, -1, -1):
        arr[i+1] = arr[i]

    arr[0] = temp

if __name__ == '__main__':

    l1 = [0, 1,2,3,4,5,6,7,8,9] # [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    left_rotate(l1)
    print l1

    l1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # [2, 3, 4, 5, 6, 7, 8, 1]
    right_rotate(l1)
    print l1
