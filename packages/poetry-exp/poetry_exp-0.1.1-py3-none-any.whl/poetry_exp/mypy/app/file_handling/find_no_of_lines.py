import re


def count_lines():
    with open('files/test2') as f:
        lines = re.findall('\n', f.read())
        print 'No of line# ', len(lines) + 1  # 1 For last line

if __name__ == '__main__':
    count_lines() # 3