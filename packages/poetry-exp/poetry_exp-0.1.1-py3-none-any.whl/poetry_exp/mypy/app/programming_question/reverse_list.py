
"""
We swap the first and last characters,
then the second and second-to-last characters, and so on until we reach the middle.

"""

# In place reverse list
def reverser_arr(arr):
    li = 0
    ri = len(arr)-1
    while li < ri:
        # swap
        arr[li], arr[ri] = arr[ri], arr[li]
        # move towards
        ri -= 1
        li += 1



# Not a in place reverse
def reverse(arr):
    return arr[::-1]


def reverse_words(message):
    li = 0
    ri = 0
    for i in range(0, len(message)):
        if message[i] == ' ':
            ri = i-1
            while li<ri:
                message[li], message[ri] = message[ri], message[li]
                li +=1
                ri -=1

            li = i+1

    print message

if __name__ == '__main__':

    a = [1, 2, 3, 4, 5, 6]
    reverser_arr(a)
    print a  # [6, 5, 4, 3, 2, 1]

    c = ['a', 'b', 'c', 'd', 'e']
    reverser_arr(c)
    print c   # ['e', 'd', 'c', 'b', 'a']

    message = ['c', 'a', 'k', 'e', ' ',
           'p', 'o', 'u', 'n', 'd', ' ',
           's', 't', 'e', 'a', 'l']
    reverse_words(message)
    print  message
    a = [1, 2, 3, 4, 5, 6]
    print reverse(a)  # [6, 5, 4, 3, 2, 1]
    print a  # [1, 2, 3, 4, 5, 6]


