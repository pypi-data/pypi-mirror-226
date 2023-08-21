
"""
Permutations and combinations, the various ways in which objects from a set may be selected,
generally without replacement, to form subsets. This selection of subsets is called a permutation
 when the order of selection is a factor, a combination when order is not a factor.

from itertools import permutations, combinations
>>> list(permutations([1,2,3], 2))
[(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

>>> list(combinations([1,2,3], 2))
[(1, 2), (1, 3), (2, 3)]


>>> list(permutations([1,2,3]))
[(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]

>>> list(combinations([1,2,3], 3))
[(1, 2, 3)]
"""

def permutations(word):
    perm_list = []
    if len(word) == 1:
        return word
    for i, letter in enumerate(word):   # word[:i] + word[i+1:]->Removes char at index i
        for perm in permutations(word[:i] + word[i+1:]):
            perm_list.append(letter + perm)
    return perm_list


def permutations2(word):
    if len(word) == 1:
        yield word
    for i, letter in enumerate(word):
        for perm in permutations2(word[:i] + word[i+1:]):
            yield letter + perm


def print_permutation(word):
    for per in permutations2(word):
        print per


if __name__ == '__main__':

    print_permutation("abc")
    print permutations("abc")

