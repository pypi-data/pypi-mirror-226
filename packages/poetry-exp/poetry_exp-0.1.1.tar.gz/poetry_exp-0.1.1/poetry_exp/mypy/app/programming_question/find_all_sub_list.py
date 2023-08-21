
def find_all_sub_list(arr):
    sub_list = []
    for i in range(len(arr)):
        j = i+1
        while j <= len(arr):
            sl = arr[i:j]
            if len(sl) > 0:
                sub_list.append(sl)
            j += 1

    return sub_list


def find_all_sub_list2(arr):
    sub_list = []
    for i in range(len(arr)):
        for j in range(i+1, len(arr)+1):
            sl = arr[i:j] # +1 because jth index not included
            if len(sl)>0:
                sub_list.append(sl)
    return sub_list


if __name__ == '__main__':
    a = [1, 2, 3, 4]
    print find_all_sub_list(a)
    print find_all_sub_list2(a)