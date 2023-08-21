from enum import Enum

class Gender(Enum):
    Male = 1
    Female = 2

# three ways to access enumeration members
print Gender.Male  # Gender.Male
print Gender(1)   # Gender.Male
print Gender['Male']  # Gender.Male


from collections import namedtuple

Person = namedtuple("Person", "gender")
p = Person(gender=Gender.Male)
print p.gender == Gender.Male
