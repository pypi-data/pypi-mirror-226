
def sub_strings(string):
    sub_strings = []
    for i in range(len(string)):
       for j in range(i+1, len(string)+1):
           sub_string = string[i:j]
           if len(sub_string)>0:
               sub_strings.append(sub_string)

    print "SubStrings: ", sub_strings, "Len: ", len(sub_strings)
    return sub_string


if __name__ == '__main__':
    sub_strings("abc") # 3+2+1 = 6
    sub_strings("abcd") # 4+3+2+1 = 10

    # No of sub string = sum of 1+2+3.....n, n*(n+1)/2
    n=3
    s1 = n*(n+1)/2
    n=4
    s2 = n*(n+1)/2
    print s1
    print s2

"""
SubStrings:  ['a', 'ab', 'abc', 'b', 'bc', 'c'] Len:  6
SubStrings:  ['a', 'ab', 'abc', 'abcd', 'b', 'bc', 'bcd', 'c', 'cd', 'd'] Len:  10
6
10
"""