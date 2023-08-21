
def first_repeating_element(arr):
    for a in arr:
        if arr.count(a) > 1:
            return a

def first_non_repeating_element(arr):
    for a in arr:
        if arr.count(a) == 1:
            return a


if __name__ == '__main__':
    a = [10, 5, 3, 4, 3, 5, 6]

    print first_repeating_element(a) # 5
    print first_non_repeating_element(a)  # 10

    a = [10, 3, 5, 3, 4, 3, 5, 6]
    print first_repeating_element(a)  # 3

