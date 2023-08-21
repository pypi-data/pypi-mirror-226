"""
A hash value of the key is computed using a hash function,
The hash value addresses a location in an array of buckets or collision lists which contains the (key , value)

"""

dict1 = {"a": 10, "b": 20, "c": 30}
dict2 = {k: v+1 for k, v in dict1.items()}

print dict2 # {'a': 11, 'c': 31, 'b': 21}

dict3 = {k+"N": v+1 for k, v in dict1.items()}
print dict3  # {'bN': 21, 'cN': 31, 'aN': 11}

# You can also quickly switch keys and values of a dictionary
dict4 = {v:k for k,v in dict1.items()}
print dict4  # {10: 'a', 20: 'b', 30: 'c'}
