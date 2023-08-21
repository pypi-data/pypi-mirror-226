from collections import Counter


def find_dup_num_from_list(l):
    return [k for k, v in Counter(l).items() if v==2]


def print_duplicates(arr):
    d = {}
    for i in range(0, len(arr)):
        freq = d.get(arr[i], 0)+1
        d[arr[i]] = freq

    for k, v in d.items():
        print k, 'comes ', v , 'times'
    return d


def find_duplicates(arr):
    dup = []
    for item in arr:
        if arr.count(item)>1:
            if dup.count(item) == 0:
                dup.append(item)

    return dup


def find_all_duplicates(arr):
    # Duplicate index return [i for i in range(0, len(arr)) if arr.count(arr[i])>1]
   return [item for item in arr if arr.count(item)>1]


def remove_duplicates(arr):
    unique_list = []
    for a in arr:
        if not a in unique_list:
            unique_list.append(a)
    return unique_list


def remove_duplicates2(arr):
    from collections import OrderedDict
    return list(OrderedDict.fromkeys(arr))


def remove_duplicates_in_place(arr):
    for i, a in enumerate(arr):
        if arr.count(a)>1:
            del arr[i]


if __name__ == '__main__':
    a = [1,3,5,2,4,5,2,3,6,8]
    print_duplicates(a)

    print find_all_duplicates(a) # [3, 5, 2, 5, 2, 3]
    print find_duplicates(a) # [3, 5, 2]

    print remove_duplicates2(a) # [1, 3, 5, 2, 4, 6, 8]
    print remove_duplicates(a)  # [1, 3, 5, 2, 4, 6, 8]
    #print set(a)
    print a

    a = [1,3,5,2,4,5,2,3,6,8]
    remove_duplicates_in_place(a)
    print a

