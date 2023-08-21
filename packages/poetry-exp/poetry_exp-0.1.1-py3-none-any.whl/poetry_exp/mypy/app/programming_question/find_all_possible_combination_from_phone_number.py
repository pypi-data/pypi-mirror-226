import itertools
latter_dict = {

    '0': '0',
    '1': '1',
    '2': "abc",
    '3': "def",
    '4': "ghi",
    '5': "jkl",
    '6': "mno",
    '7': "pqrs",
    '8': "tuv",
    '9': "wxyz"

}


def possible_words(phone_number):
    words = []
    latters_to_combine = [latter_dict[digit] for digit in phone_number]
    print latters_to_combine  # ['1', 'abc', 'def', 'ghi', 'jkl', '0']

    for letters_group in itertools.product(*latters_to_combine):
        #print letters_group
        words.append("".join(letters_group))

    return words

# ToDO try printing all combiniation without using itertools

if __name__ == '__main__':
    words = possible_words("123450")
    words.sort()
    print (",".join(words))

    for w in itertools.product(*['1','ac', 'de']):
        print w

"""
('1', 'a', 'd')
('1', 'a', 'e')
('1', 'c', 'd')
('1', 'c', 'e')
"""

for w in itertools.product(['1', 'ac', 'de']):
    print w

"""
('1',)
('ac',)
('de',)
"""
