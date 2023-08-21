import os
import fileinput


# for small file
def replace_char_in_file(file_path, replace_char, new_char):
    with open(file_path) as f:
        file_contents = f.read()
        new_contents = file_contents.replace(replace_char, new_char)

    with open(file_path, 'w') as f:
        f.write(new_contents)


def replace_char_in_file3(file_path, replace_char, new_char):
    import re
    with open(file_path) as f:
        output = re.sub(replace_char, new_char, f.read())
    print output
    with open(file_path, 'w') as f:
        f.write(output)


def replace_char_in_file2(file_path, replace_char, new_char):
    import fileinput
    for line in fileinput.FileInput(file_path, inplace=True):
        line = line.replace(replace_char, new_char)
        print line


def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


if __name__ == '__main__':
    #replace_char_in_file('files/test1.txt', ',', ":")
    replace_char_in_file2('files/test1.txt', 'aafak', "aafak2")


                             



