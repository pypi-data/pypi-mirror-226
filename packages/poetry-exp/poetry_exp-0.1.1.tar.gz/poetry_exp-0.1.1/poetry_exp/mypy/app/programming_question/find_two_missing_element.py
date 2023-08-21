from collections import Counter
from array import array

def find_missing_elements(l, start, end):
    d = Counter(l)
    #print d
    return [num for num in range(start, end+1) if d[num] == 0]


def find_missing_elements2(l, start, end):
    return [num for num in range(start, end+1) if num not in l]


def find_missing_elements3(l, n):
    temp = [0]*(n+1) # because we are not cheking 0
    for item in l:
        temp[item] = item
    return [i for i in range(1, n) if temp[i]==0]
   # o(n) + o(n) = O(2N), in big o notation o(N)


if __name__ == '__main__':
    print find_missing_elements([1, 3, 5, 6, 9, 10], 1, 10)  # [2, 4, 7, 8]
    print find_missing_elements([6, 9, 10,1, 3, 5], 1, 10)  # [2, 4, 7, 8]

    print find_missing_elements3([6, 9, 10,1, 3, 5], 10)  # [2, 4, 7, 8]
