
"""
Find the element that appears once in an array where every other element appears twice
Given an array of integers. All numbers occur twice except one number which occurs once. Find the number in O(n) time & constant extra space.

Example :

Input:  ar[] = {7, 3, 5, 4, 5, 3, 4}
Output: 7
One solution is to check every element if it appears once or not. Once an an element with single occurrence is found, return it. Time complexity of this solution is O(n2).

A better solution is to use hashing.
1) Traverse all elements and put them in a hash table. Element is used as key and count of occurrences is used as value in hash table.
2) Traverse the array again and print the element with count 1 in hash table.
This solution works in O(n) time, but requires extra space.


Another approach:
This is not an efficient approach but just another way to get the desired results.
If we add each number once and multiply the sum by 2, we will get twice sum of each element of the array.
 Then we will subtract the sum of the whole array from the twice_sum and get the required number
(which appears once in the array).



Array [] : [a, a, b, b, c, c, d]
In more simple words: 2*(some of arrays) - sum -f arrays
let arr[] = {7, 3, 5, 4, 5, 3, 4}
Required no = 2*(sum_of_array_without_duplicates) - (sum_of_array)
            = 2*(7 + 3 + 5 + 4) - (7 + 3 + 5 + 4 + 5 + 3 + 4)
            = 2*     19         -      31
            = 38 - 31
            = 7 (required answer)
"""


#  [k for k, v in Counter(arr).items() if v==1]
def find_element_that_appears_once(arr):
    item_dict = {}
    for a in arr:
        if a in item_dict:
            item_dict.update({a: item_dict.get(a) + 1})
        else:
            item_dict.update({a: 1})

    for k, v in item_dict.items():
        if v == 1:
            return k


if __name__ == '__main__':
    l = [7, 3, 5, 4, 5, 3, 4]
    print find_element_that_appears_once(l) # 7
    