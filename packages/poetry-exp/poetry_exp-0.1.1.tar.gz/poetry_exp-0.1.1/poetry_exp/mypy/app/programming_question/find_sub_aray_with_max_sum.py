
def find_sub_arrays(arr):
    sub_list = list()
    for i in range(len(arr)):
        j = i+1
        while j <= len(arr):

            sl = arr[i:j]

            if len(sl) > 1:
                sub_list.append(sl)
            j += 1

    return sub_list


def find_sub_array_with_max_sum(arr):
    sub_arrays = find_sub_arrays(arr)
    max_sum_sub_arr = sub_arrays[0]
    for sub_array in sub_arrays[1:]:
        if sum(sub_array) > sum(max_sum_sub_arr):
            max_sum_sub_arr = sub_array

    return max_sum_sub_arr


if __name__ == '__main__':

    a = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print find_sub_array_with_max_sum(a) # [4, -1, 2, 1], sum is 6



