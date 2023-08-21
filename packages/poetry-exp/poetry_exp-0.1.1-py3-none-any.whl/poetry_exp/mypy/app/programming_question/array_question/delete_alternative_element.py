import copy


def find_alt_item(arr):
    return arr[::2]


def delete_alt_item(arr):
    return [item for i, item in enumerate(arr) if i % 2 == 0]


def delete_alt_item_in_place(arr):
    temp = copy.copy(arr)
    index = 0
    for item in temp:
        if index %2 == 1:
            arr.remove(item)
        index += 1


# Without using copy
def delete_alt_item_in_place2(arr):
    index = 0
    for item in arr:
        if index %2 == 1:
            del arr[index]
        index += 1


if __name__ == '__main__':
    a1 = [10, 20, 30, 40, 50, 60]
    print delete_alt_item(a1) # [10, 30, 50]
    print a1 # [10, 20, 30, 40, 50, 60]

    a1 = [10, 20, 30, 40, 50, 60]
    delete_alt_item_in_place(a1)
    print a1 # [10, 30, 50]

    a1 = [20, 10, 20, 10, 30, 40, 20, 50, 60]
    delete_alt_item_in_place(a1)
    print a1  # [20, 20, 30, 20, 60]

    a1 = [10, 20, 30, 40, 50, 60]
    delete_alt_item_in_place2(a1)
    print a1  # [10, 30, 50]
