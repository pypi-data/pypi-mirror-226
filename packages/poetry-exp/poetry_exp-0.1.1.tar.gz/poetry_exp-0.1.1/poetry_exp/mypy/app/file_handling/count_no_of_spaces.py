import re


def find_no_of_char(char):
    with open('files/test1') as f:
       chars = re.findall(char, f.read())
       if chars:
           print 'No. of char: {0} in file is {1}'.format(char, len(chars))


def find_no_of_char2(char):
    with open('files/test1') as f:
       print 'No. of char: {0} in file is {1}'.format(char, f.read().count(char))


if __name__ == '__main__':
    find_no_of_char(' ') # 6
    find_no_of_char('s') # 4

    find_no_of_char2(' ')  # 6
    find_no_of_char2('s')  # 4


"""
No. of char:   in file is 6
No. of char: s in file is 4
No. of char:   in file is 6
No. of char: s in file is 4
"""