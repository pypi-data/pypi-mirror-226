
def find_all_num():
    import re
    with open('files/test2') as f:
        nums = re.findall('\d', f.read())
        print nums


if __name__ == '__main__':
    print find_all_num()
    # ['1', '2', '9', '7', '3', '1', '5', '1', '9', '9', '2', '2', '2', '2', '9']
