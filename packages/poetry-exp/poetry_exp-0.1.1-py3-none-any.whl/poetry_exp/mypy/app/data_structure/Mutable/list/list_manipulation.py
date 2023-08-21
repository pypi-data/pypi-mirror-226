l1 = [1, 2, 3]
l2 = [2, 3]

# l3 = l1-l2  # TypeError: unsupported operand type(s) for -: 'list' and 'list'
# print l3,  For this you should use set

l3 = l1 + l2
print l3  # [1, 2, 3, 2, 3]
#l3  = l1 + 1  # TypeError: can only concatenate list (not "int") to list

#l4 = l1 * l2  # TypeError: can't multiply sequence by non-int of type 'list'

l4 = l1 * 3
print l4  # [1, 2, 3, 1, 2, 3, 1, 2, 3]

# l5 = l1/2  TypeError: unsupported operand type(s) for /: 'list' and 'int'

print l1  # [1, 2, 3]
print l2  # [2, 3]