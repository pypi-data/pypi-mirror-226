s1 = {1, 2, 3}
s2 = {2, 4, 5}

s3 = s1 - s2
print s3  # set([1, 3])

# s4 = s1 + s2  # TypeError: unsupported operand type(s) for +: 'set' and 'set'
# print s4
#s4 = s1 + 2  # TypeError: unsupported operand type(s) for +: 'set' and 'int'

s4 = s1.union(s2)
print s4  # set([1, 2, 3, 4, 5])   # ignore the duplicates

