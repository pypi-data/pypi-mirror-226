"""
Reverse words in a given String in Python
We are given a string and we need to reverse words of given string ?

Examples:

Input : str = "geeks quiz practice code"
Output : str = "code practice quiz geeks"
"""


def reverse_word(s):
    rev_words = []
    words = s.split()
    for i in range(len(words)-1, -1, -1):
        rev_words.append(words[i])
    return " ".join(rev_words)


def reverse_word2(s):
    words = s.split()
    l = 0
    r =len(words) - 1
    while l < r:
        words[l], words[r] = words[r], words[l]
        l += 1
        r -=1

    return " ".join(words)


def reverseWords(input):
    # split words of string separated by space
    inputWords = input.split(" ")

    # reverse list of words
    # suppose we have list of elements list = [1,2,3,4],
    # list[0]=1, list[1]=2 and index -1 represents
    # the last element list[-1]=4 ( equivalent to list[3]=4 )
    # So, inputWords[-1::-1] here we have three arguments
    # first is -1 that means start from last element
    # second argument is empty that means move to end of list
    # third arguments is difference of steps
    inputWords = inputWords[-1::-1] # generates new list

    # now join words with space
    output = ' '.join(inputWords)

    return output

if __name__ == '__main__':
    str = "geeks quiz practice code"
    print reverse_word(str)

    str = "geeks quiz practice code"
    print reverse_word2(str)

    str = "geeks quiz practice code"
    print reverseWords(str)