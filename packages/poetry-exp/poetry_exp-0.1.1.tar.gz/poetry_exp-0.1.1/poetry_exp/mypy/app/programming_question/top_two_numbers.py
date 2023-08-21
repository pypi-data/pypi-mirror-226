

def find_top_two_number(arr):
    largest = arr[0]
    second_largest = arr[1]

    for i in range(0, len(arr)):
        if arr[i] > largest:
            second_largest = largest
            largest = arr[i]
        elif arr[i] > second_largest:
            second_largest = arr[i]

    return largest, second_largest

"""
Assumption: List doest not have duplicates
"""

if __name__ == '__main__':
    a = [10,11,1, 3, 5, 7, 9, 2, 4, 6, 8, 10, 15, 13]

    print find_top_two_number(a)