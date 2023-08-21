"""
The basic difference is:
instance variables are for data which is unique to every object
Class variables are for data shared between different instances of a class

"""


class Cal(object):
    # pi is a class variable
    pi = 3.142

    def __init__(self, radius):
        # self.radius is an instance variable
        self.radius = radius

    def area(self):
        return self.pi * (self.radius ** 2)


a = Cal(32)
print a.area()  # Output: 3217.408

# Misuse
print a.pi  # 3.142

a.pi = 2
print a.area()  # 2048

b = Cal(32)
print b.area()  # Output: 3217.408
print b.pi  # Output: 3.142  # but pi is type of list, then it will be 2
b.pi = 50
print b.pi  # Output: 50


class SuperClass(object):
    superpowers = []  # if any one instance changes it , it will reflect in all the instance

    def __init__(self, name):
        self.name = name

    def add_superpower(self, power):

        self.superpowers.append(power)


foo = SuperClass('foo')
bar = SuperClass('bar')
print foo.name # Output: 'foo'
print bar.name # Output: 'bar'
foo.add_superpower('fly')
print bar.superpowers  # Output: ['fly'] # That is the beauty of the wrong usage of mutable class variables
print foo.superpowers  # Output: ['fly'] # That is the beauty of the wrong usage of mutable class variables
