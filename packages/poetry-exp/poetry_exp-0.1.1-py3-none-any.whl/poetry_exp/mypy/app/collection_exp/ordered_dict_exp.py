"""
OrderedDict keeps its entries sorted as they are initially inserted. Overwriting a value
of an existing key does not change the position of that key. However, deleting and
reinserting an entry moves the key to the end of the dictionary

"""



from collections import OrderedDict


colours = {"Red": 198, "Green": 170, "Blue": 160}
for key, value in colours.items():
   print(key, value)

'''
OUTPUT:
('Blue', 160)
('Green', 170)
('Red', 198)
'''

colours = OrderedDict()
colours.update({"Red": 198})
colours.update({"Green": 198})
colours.update({"Blue": 198})
print colours  # OrderedDict([('Red', 198), ('Green', 198), ('Blue', 198)])
for key, value in colours.items():
   print(key, value)

"""
Output:
('Red', 198)
('Green', 198)
('Blue', 198)
"""

colours = OrderedDict([("Red", 198), ("Green", 170), ("Blue", 160)])
for key, value in colours.items():
   print(key, value)