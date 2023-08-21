a = {"A":{"n1":1}, "B":{"n2":2}}

b = {}
b['myA'] = a['A']
b['myB'] = a['B']

del a
print b