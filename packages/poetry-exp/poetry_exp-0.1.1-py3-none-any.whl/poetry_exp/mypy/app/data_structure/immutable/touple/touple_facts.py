l = [1, 2, 3]
t = (1, 2, l)
print t  # (1, 2, [1, 2, 3])

l.append(4)  # will work because, touple stores the reference not the list object, so no change in the reference
# So adding the element in the list will not change anything in the touple
# Touple
t[2].append(5)
print t  # (1, 2, [1, 2, 3, 4, 5])
