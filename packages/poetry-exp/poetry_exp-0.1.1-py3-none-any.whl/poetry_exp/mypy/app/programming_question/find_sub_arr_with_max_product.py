
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


def product(arr):
    return reduce(lambda x, y: x*y, arr)


def find_sub_array_with_max_product(arr):
    sub_arrays = find_sub_arrays(arr)
    max_product_sub_arr = sub_arrays[0]
    for sub_array in sub_arrays[1:]:
        if product(sub_array) > product(max_product_sub_arr):
            max_product_sub_arr = sub_array

    return max_product_sub_arr

# 25, 26, 18, 17
if __name__ == '__main__':

    a = [2, 3, -2, 4]
    print find_sub_array_with_max_product(a) # [2, 3], product is 6

