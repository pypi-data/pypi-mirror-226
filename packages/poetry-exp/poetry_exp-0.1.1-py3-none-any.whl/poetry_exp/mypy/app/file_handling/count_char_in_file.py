def count_char(file_name, char):
    count = 0
    file = open(file_name, "r")
    for i in file:
        for c in i:
            if c == char:
                count = count + 1
    print("THE CHARACTER {} IS FOUND {} TIMES IN THE TEXT FILE".format(char, count))


if __name__ == '__main__':
    count_char('map2.txt', '1')