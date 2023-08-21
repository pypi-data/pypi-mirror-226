from werkzeug.datastructures import ImmutableMultiDict
imd = ImmutableMultiDict([('name', 'Aafak'), ('name', 'Ajay'), ('Age', 23)])
print imd # ImmutableMultiDict([('Age', 23), ('name', 'Aafak'), ('name', 'Ajay')])

print imd.to_dict()  #  {'Age': 23, 'name': 'Aafak'}
print imd.to_dict(flat=False)  # {'Age': [23], 'name': ['Aafak', 'Ajay']}