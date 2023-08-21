from collections import defaultdict

"""
defaultdict is a sub class of dict with a default value factory
"""
colours = (
    ('Yasoob', 'Yellow'),
    ('Ali', 'Blue'),
    ('Arham', 'Green'),
    ('Ali', 'Black'),
    ('Yasoob', 'Red'),
    ('Ahmed', 'Silver'),
)

print type(colours) # <type 'tuple'>
print colours[0] # ('Yasoob', 'Yellow')
print colours[0][0] # Yasoob

fav_colurs = defaultdict(str)

for name, colour in colours:
    fav_colurs[name] = colour

print fav_colurs  # defaultdict(<type 'str'>, {'Arham': 'Green', 'Yasoob': 'Red', 'Ahmed': 'Silver', 'Ali': 'Black'})
# From here we can see value for key Yasoob is updated with new values, it overrides

# To avoid overrides, use defaultdict with list

fav_colurs = defaultdict(list)

for name, colour in colours:
    fav_colurs[name].append(colour)

print fav_colurs   # defaultdict(<type 'list'>, {'Arham': ['Green'], 'Yasoob': ['Yellow', 'Red'], 'Ahmed': ['Silver'], 'Ali': ['Blue', 'Black']})


# Problem in normal dict
some_dict = {}
#some_dict['colours']['favourite'] = "yellow"
# Raises KeyError: 'colours

# Solution
tree = lambda : defaultdict(tree)
d = tree()
d['colours']['favourite'] = "yellow"
print d  # defaultdict(<function <lambda> at 0x00000000034CCF98>, {'colours': defaultdict(<function <lambda> at 0x00000000034CCF98>, {'favourite': 'yellow'})})
print d['colours']['favourite'] # yellow
import json
print json.dumps(d)

for k,v in d.items():
    print k, v


colours2 = [
    ['Yasoob', 'Yellow'],
    ['Ali', 'Blue'],
    ['Arham', 'Green'],
    ['Ali', 'Black'],
    ['Yasoob', 'Red'],
    ['Ahmed', 'Silver'],
]

print type(colours2) # <type 'list'>
print colours2[0] # ['Yasoob', 'Yellow']
print colours2[0][0] # Yasoob