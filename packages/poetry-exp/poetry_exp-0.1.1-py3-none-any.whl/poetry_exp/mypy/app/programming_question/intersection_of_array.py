
def get_common(arr1, arr2):
    common = []
    for a in arr1:
        if a in arr2:
            common.append(a)
    return common


def find_intersection(arr1, arr2):
    return [x for x in arr1 if x in arr2]
    #return get_common(arr1, arr2) if len(arr1) > len(arr2) else get_common(arr2, arr1)


if __name__ == '__main__':
    a1 = [10, 20, 30, 50, 60]
    a2 = [70, 30, 80, 10]

    print find_intersection(a1, a2) # 10, 30
    print find_intersection(a2, a1)  # 10, 30
