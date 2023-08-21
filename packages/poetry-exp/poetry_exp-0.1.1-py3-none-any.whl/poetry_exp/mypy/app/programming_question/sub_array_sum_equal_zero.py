
def find_sub_arrays(arr):
    sub_list = []
    for i in range(len(arr)):
        j = i+1
        while j <= len(arr):
            sl = arr[i:j]
            if len(sl) > 1:
                sub_list.append(sl)
            j += 1
    return sub_list


def is_sub_arr_sum_equal_zero(arr):
    sub_arrays = find_sub_arrays(arr)
    for sub_array in sub_arrays:
        if sum(sub_array) == 0:
            return sub_array
    return []


if __name__ == '__main__':
    arr = [4, 2, -3, 1, 6]

    print (is_sub_arr_sum_equal_zero(arr))
