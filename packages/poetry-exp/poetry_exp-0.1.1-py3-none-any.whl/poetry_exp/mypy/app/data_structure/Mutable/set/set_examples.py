# Set is similar to list with the distinction that they cannot contail duplicate values
# Set can be used to remove duplicates from the list , e.g set([])

non_dup = set([1,2,3,1,5,2,3,1])
print non_dup #set([1, 2, 3, 5])
print list(non_dup)
for i in non_dup:
    print i

# Intersection
set_a = set([10,20,30,40,50]) # or {10,20,30,40,50}
set_b = set([10,30,50,70])   # or {10, 30, 50, 70}

print set_a.intersection(set_b) # set([10, 50, 30])
print set_a.difference(set_b) # set([40, 20]) Which are in A not in B
print set_b.difference(set_a) # set([70])
