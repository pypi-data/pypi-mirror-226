"""
Majority Element
Write a function which takes an array and prints the majority element (if it exists),
otherwise prints No Majority Element. A majority element in an array A[] of size n is
an element that appears more than n/2 times (and hence there is at most one such element).
Examples :

Input : {3, 3, 4, 2, 4, 4, 2, 4, 4}
Output : 4

Input : {3, 3, 4, 2, 4, 4, 2, 4}
Output : No Majority Element
"""


def find_majority_element(arr):
    item_dict = {}

    for a in arr:
        if a in item_dict:
            item_dict.update({a: item_dict.get(a) + 1})
            if item_dict.get(a) > len(arr)/2:
                print 'Majority element is: ', a
                return a
        else:
            item_dict.update({a: 1})


if __name__ == '__main__':

    a = [2, 2, 2, 2, 5, 5, 2, 3, 3]
    print find_majority_element(a)

    a2 = [3, 3, 4, 2, 4, 4, 2, 4, 4]
    print find_majority_element(a2)

    a3 = [3, 3, 4, 2, 4, 4, 2, 4]
    print find_majority_element(a3)
