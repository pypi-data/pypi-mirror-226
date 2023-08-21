
items = [10,20,30,40]

for item in items:
    items[1] = 100 # modify
    #print item

"""
10
100
30
40
"""

for item in items:
    # items.append(100) # add, will add every time comes to loop, which will make it never ending this
    # print item
    pass

"""
 Above code will enter into infinite loop
"""

items = [10,20,30,40]
for item in items:
    if item == 10:
       del item # delete
#print(items)  # [10, 20, 30, 40]

items = [
    {"id": 1},
    {"id": 2},
    {"id": 3},
    {"id": 4}
]
for item in items:
    if item['id'] == 2:
       del item # delete
#print(items)  # [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}]



items = [
    {"id": 1},  # 0
    {"id": 2},  # 1, 0
    {"id": 3},  # 2, 1
    {"id": 4}   # 3, 2
]
for i, item in enumerate(items):
    #print(i)
    if item['id'] == 2 or item['id'] == 3:
       items.pop(i)
#print(items)  # [{'id': 1}, {'id': 3}, {'id': 4}]  #!!!!Wrong result

items = [
    {"id": 1},  # 0
    {"id": 2},  # 1, 0
    {"id": 3},  # 2, 1
    {"id": 4}   # 3, 2
]
for i, item in enumerate(items.copy()):
    #print(i)
    if item['id'] == 2 or item['id'] == 3:
       items.pop(i)
# print(items)  # [{'id': 1}, {'id': 3}]   #!!!!Wrong result

items = [
    {"id": 1},  # 0
    {"id": 2},  # 1, 0
    {"id": 3},  # 2, 1
    {"id": 4}   # 3, 2
]

items = [item for item in items if item['id'] != 2 and item['id'] != 3]
# print(items) # correct

items = [
    {"id": 1, 'assetInfo':[{'type': "A"},{'type': 'A'}]},
    {"id": 2, 'assetInfo':[{'type': "B"},{'type': 'B'}]},
    {"id": 3, 'assetInfo':[{'type': "C"},{'type': 'C'}]},
    {"id": 4, 'assetInfo':[{'type': "B"},{'type': 'B'}]}
]

items = [item for item in items if [asset for asset in item['assetInfo'] if asset['type']=='B']]
print(items) # [{'id': 2, 'assetInfo': [{'type': 'B'}, {'type': 'B'}]}, {'id': 4, 'assetInfo': [{'type': 'B'}, {'type': 'B'}]}]
