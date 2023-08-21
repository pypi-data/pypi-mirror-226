"""
Remove all duplicates from a given string in Python
We are given a string and we need to remove all duplicates from it ? What will be the output if order of character matters ?
Examples:

Input : geeksforgeeks
Output : efgkos


OrderedDict:
Method fromkeys() creates a new dictionary with keys from seq and values
 set to value and returns list of keys, fromkeys(seq[, value]) is the syntax for fromkeys() method.
Parameters :
seq : This is the list of values which would be used for dictionary keys preparation.
value : This is optional, if provided then value would be set to this value.

from collections import OrderedDict
seq = ('name', 'age', 'gender')
dict = OrderedDict.fromkeys(seq)

# Output = {'age': None, 'name': None, 'gender': None}
print str(dict)
dict = OrderedDict.fromkeys(seq, 10)

# Output = {'age': 10, 'name': 10, 'gender': 10}
print str(dict)
"""


# set does not maintain order
def remove_dup(s):
    return "".join(set(s))


def remove_dup_with_order(s):
    from collections import OrderedDict
    return "".join(OrderedDict.fromkeys(s))

def remove_duplicate_char(s):
    chars = []
    for c in s:
        if not c in chars:
            chars.append(c)
    return "".join(chars)


if __name__ == '__main__':
    s = "geeksforgeeks"
    print remove_dup(s)
    print remove_dup_with_order(s)


"""
egfkosr
geksfor
"""