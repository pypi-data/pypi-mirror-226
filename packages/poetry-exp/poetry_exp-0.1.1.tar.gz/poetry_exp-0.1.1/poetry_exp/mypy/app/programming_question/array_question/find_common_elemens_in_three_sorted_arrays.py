

def find_common_element(arr1, arr2):
    n1 = len(arr1)
    n2 = len(arr2)
    i = 0
    j = 0
    while i<n1 and j<n2:
        if arr1[i] == arr2[j]:
            print arr1[i]
            i +=1
            j+=1
        elif arr1[i] > arr2[j]:
            j +=1
        else:
            i +=1

    print '..................'


if __name__ == '__main__':
    a1 = [1 ,2 ,3, 4]
    a2 = [2, 4, 6, 8]
    find_common_element(a1, a2)  # 2, 4
    find_common_element(a2, a1)  # 4, 2

    a1 = [6, 8, 10, 12, 15]
    a2 = [2, 4, 6, 8, 15]
    find_common_element(a1, a2)  # 6, 8, 15