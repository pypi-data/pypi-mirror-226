
"""

Without a doubt, when writing a class you'll always want to go for new-style classes.
The perks of doing so are numerous, to list some of them:

Support for descriptors. Specifically, the following constructs are made possible with descriptors:

classmethod: A method that receives the class as an implicit argument instead of the instance.
staticmethod: A method that does not receive the implicit argument self as a first argument.
properties with property: Create functions for managing the getting, setting and deleting of an attribute.
__slots__: Saves memory consumptions of a class and also results in faster attribute access. Of course, it does impose limitations.
The __new__ static method: lets you customize how new class instances are created.

Method resolution order (MRO): in what order the base classes of a class will be searched when trying to resolve which
                               method to call.

Related to MRO, super calls. Also see, super() considered super.

If you don't inherit from object, forget these.
"""


# Following will not work without inheriting the Object class
class Singleton(object):

    def __new__(cls, *args, **kwargs):
        print 'creating object...'
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


s = Singleton()


class Singleton2:

    def __new__(cls, *args, **kwargs):
        print 'creating object...'
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


s = Singleton2()


class WithoutSlotTest(object):

    def __init__(self, name, dob):
        self.name=name
        self.dob=dob


class SlotTest(object):  # without inheriting the object class , its not possible
    __slots__ = ['name', 'dob']

    def __init__(self, name, dob):
        self.name=name
        self.dob=dob


s = WithoutSlotTest('a', '1/2/98')
print s.__dict__  # {'dob': '1/2/98', 'name': 'a'}, stores the instance attribute

s = SlotTest('a', '1/2/98')
print s.__dict__  #AttributeError: 'SlotTest' object has no attribute '__dict__'

