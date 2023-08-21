
item_list = [1, 3, 5, 2, 4, 1, 5, 2, 4, 7]
duplicates = []

for item in item_list:
    if item_list.count(item)>1:
        if not item in duplicates:
            duplicates.append(item)

print duplicates


# using list comprehension
item_list = [1, 3, 5, 2, 4, 1, 5, 2, 4, 7]

duplicates = [item for item in item_list if item_list.count(item)>1]
print set(duplicates)

# duplicates = set([item for item in item_list if item_list.count(item)>1])


def is_num_duplicate(arr, num):
    d = {}
    for a in arr:
        if a in d:
            d.update({a: d.get(a) + 1})
        else:
            d.update({a: 1})

    if d.get(num) > 1:
        print num, 'is duplicate'
    else:
        print num, 'is not duplicate'


def is_arr_contains_duplicate(arr):
    d = {}
    for a in arr:
        if a in d:
            d.update({a: d.get(a) + 1})
        else:
            d.update({a: 1})

    if sum(d.values()) > len(d):
        print arr, 'contains duplicates'
    else:
        print arr, ' does not contains duplicate'


# just detect duplicate
def is_arr_contains_duplicate2(arr):
    return len(set(arr)) == len(arr)


print is_arr_contains_duplicate2([1, 2, 3, 4])  # True
print is_arr_contains_duplicate2([1, 2, 3, 4, 1]) # False


is_arr_contains_duplicate([1, 2, 3])
is_arr_contains_duplicate([1, 2, 3, 1, 4])
is_arr_contains_duplicate([1, 2, 3, 6, 7, 8])
is_arr_contains_duplicate([1, 2, 3, 5, 3, 6])


is_num_duplicate([1, 3, 5, 2, 4, 2], 1)
is_num_duplicate([1, 3, 5, 2, 4, 2], 3)
is_num_duplicate([1, 3, 5, 2, 4, 2], 5)
is_num_duplicate([1, 3, 5, 2, 4, 2], 2)



