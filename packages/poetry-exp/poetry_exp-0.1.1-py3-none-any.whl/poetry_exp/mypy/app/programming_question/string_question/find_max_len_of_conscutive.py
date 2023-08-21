"""
Maximum length of consecutive 1s in a binary string in Python using Map function
We are given a binary string containing 1s and 0s. Find maximum length of consecutive 1s in it.

Examples:

Input : str = '11000111101010111'
Output : 4

We have existing solution for this problem please refer Maximum consecutive ones (or zeros)
in a binary array link. We can solve this problem within single line of code in Python. Approach is very simple,

Separate all sub-strings of consecutive 1s separated by zeros using split() method of string.
Print maximum length of splited sub-strings of 1s.

# input.split('0') --> splits all sub-strings of consecutive 1's
# separated by 0's, output will be like ['11','1111','1','1','111']
# map(len,input.split('0'))  --> map function maps len function on each
# sub-string of consecutive 1's
# max() returns maximum element from a list
"""

def max_len_con(s):
    consutive_ones = s.split("0")
    return max(map(len, consutive_ones))


if __name__ == '__main__':

    str = '11000111101010111'
    print max_len_con(str) # 4