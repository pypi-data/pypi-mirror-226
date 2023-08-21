import re


def find_word_count(word):
    with open('files/test1') as f:
        words = re.findall('\\b' + word + '\\b', f.read())
        # words = re.findall(word, f.read()) will return 2
        print 'Word Count # ', len(words)


def find_words_count_in_file():
    with open('files/test1') as f:
        words = re.findall('\\b[\w@_-]+\\b', f.read())
        # words = re.findall(word, f.read()) will return 2
        print 'Words Count # ', len(words)


if __name__ == '__main__':
    find_word_count('this')  # 1

    find_words_count_in_file() # 8
