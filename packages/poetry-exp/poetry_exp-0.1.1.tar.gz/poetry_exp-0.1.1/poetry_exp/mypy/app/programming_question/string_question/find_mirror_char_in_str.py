"""
Python Dictionary to find mirror characters in a string

Given a string and a number N, we need to mirror the characters from N-th position
up to the length of the string in the alphabetical order. In mirror operation,
 we change a to z, b to y, and so on.

Examples:

Input : N = 3
        paradox
Output : paizwlc
We mirror characters from position 3 to end.

Input : N = 6
        pneumonia
Output : pnefnlmrz
"""


def replace_by_mirror_char(str1, position):

    orignal_str = 'abcdefghijklmnopqrstuvwxyz'
    reverse_str = orignal_str[-1::-1]
    mirror_dict = dict(zip(orignal_str, reverse_str))

    prefix = str1[0:position-1]
    suffix = str1[position-1:]

    mirror = ''
    for i in range(len(suffix)):
        mirror += mirror_dict.get(suffix[i])

    return prefix + mirror


# Driver program
if __name__ == "__main__":
    s = 'paradox'
    k = 3
    print replace_by_mirror_char(s, k)  # paizwlc
