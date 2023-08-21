"""
SequenceMatcher in Python for Longest Common Substring
Given two strings X and Y, print the longest common sub-string.

Examples:

Input :  X = "GeeksforGeeks",
         Y = "GeeksQuiz"
Output : Geeks

Input : X = "zxabcdezy",
        Y = "yzabcdezx"
Output : abcdez
"""


def find_longest_common_sub_str(str1, str2):
    if len(str1) > len(str2):
        big_str = str1
        small_str = str2
    else:
        big_str = str1
        small_str = str2
    common_str_len = 0
    common_str = ''
    for i in range(len(big_str)):
        for j in range(i+1, len(big_str)+1):
            sub = big_str[i:j]
            if sub in small_str:
                if len(sub) > common_str_len:
                    common_str_len = len(sub)
                    common_str = sub

    print 'common sub string: ', common_str


if __name__ == '__main__':
    s1 = 'GeeksforGeeks'
    s2 = 'GeeksQuiz'
    find_longest_common_sub_str(s1, s2)  # Geeks

    s1 = 'zxabcdezy'
    s2 = 'yzabcdezx'
    find_longest_common_sub_str(s1, s2)  # abcdez
