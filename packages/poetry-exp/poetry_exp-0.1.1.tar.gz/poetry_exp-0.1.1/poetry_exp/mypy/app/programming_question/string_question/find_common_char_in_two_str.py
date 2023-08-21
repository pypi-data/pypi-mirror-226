"""
Python code to print common characters of two Strings in alphabetical order
Given two strings, print all the common characters in lexicographical order. If there are no common letters, print -1. All letters are lower case.

Examples:

Input :
string1 : geeks
string2 : forgeeks
Output : eegks
Explanation: The letters that are common between
the two strings are e(2 times), k(1 time) and
s(1 time).
Hence the lexicographical output is "eegks"

Input :
string1 : hhhhhello
string2 : gfghhmh
Output : hhh

"""


def find_common_char(str1, str2):

    if len(str1) > len(str2):
        big_str = str1
        small_str = str2
    else:
        big_str = str2
        small_str = str1

    return "".join(sorted([s for s in small_str if s in big_str]))


def find_common_char2(str1, str2):

    if len(str1) > len(str2):
        big_str = str1
        small_str = str2
    else:
        big_str = str2
        small_str = str1

    for s in big_str:
        if not s in small_str:
            print s, 'needs to be removed'
            
if __name__ == '__main__':
    s1 = "geeks"
    s2 = "forgeeks"

    print find_common_char(s1, s2) # eegks

    string1 = 'hhhhhello'
    string2 = 'gfghhmh'
    print  find_common_char(string1, string2)  # hhh