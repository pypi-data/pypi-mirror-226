import copy


def find_smallest(arr, k):
   temp_arr = copy.copy(arr)
   for i in range(k):
       smallest = min(temp_arr)
       for i in range(temp_arr.count(smallest)):
           temp_arr.remove(smallest)
   return smallest

# Handle duplicates
def find_largets(arr, k):
   temp_arr = copy.copy(arr)
   for i in range(k):
       largest = max(temp_arr)
       for i in range(temp_arr.count(largest)):
           temp_arr.remove(largest)
   return largest


if __name__ == '__main__':
    a = [1, 2, 3, 9, 4, 1, 1]
    k = 3
    print find_smallest(a, k)  # 3
    print find_largets(a, 2)   # 4
    print a

# Do not handle duplicates
    a = [1, 3, 5, 2, 6, 4, 9]
    a.sort()
    print a[k-1]  # 3  kth smallest
    a.sort(reverse=True)
    print a[k-1]  # 5  kth largest

