"""
A tuple is basically a immutable list
which allows you to store a sequence of values separated by commas. They are just
like lists but have a few key differences. The major one is that unlike lists, you can
not reassign an item in a tuple. In order to access the value in a tuple you use integer
indexes like:
man = ('Ali', 30)
print(man[0])
# Output: Ali

namedtuples dont use integer indexes for accessing
members of a tuple. You can think of namedtuples like dictionaries but unlike dictionaries
they are immutable.
sysntax:
(touple name, touple fields)

A named tuple has two required arguments. They are
the tuple name and the tuple field_names. In the above example our tuple name was
Animal and the tuple field_names were name, age and type.  And as you are not bound to use integer indexes to access
members of a tuple, it makes it more easy to maintain your code. Moreover, as
namedtuple instances do not have per-instance dictionaries, they are lightweight
and require no more memory than regular tuples. This makes them faster than dictionaries.
However, do remember that as with tuples, attributes in namedtuples are
immutable. It means that this would not work
"""

from collections import namedtuple

animal = namedtuple('Animal', 'name age type')
perry = animal(name="peryy", age=3, type="cat")
perry2 = animal(age=3, name="peryy2", type="cat")
print perry # Animal(name='peryy', age=3, type='cat')
print perry2 # Animal(name='peryy2', age=3, type='cat')
print perry.name
print perry2.name

#perry.age = 42 # AttributeError: can't set attribute

#perry3 = animal(age=3, name="peryy3")  #TypeError: __new__() takes exactly 4 arguments (3 given)
#print perry3


"""
They are backwards compatible with normal tuples. It means that you can use integer indexes with
namedtuples as well:
"""

print perry[0] # peryy

# you can convert a namedtuple to a dictionary
print perry._asdict() # OrderedDict([('name', 'peryy'), ('age', 3), ('type', 'cat')])