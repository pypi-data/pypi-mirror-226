
"""
@staticmethod: Used to defines some utility methods inside a class, which does not requires object instance

When to use what?
We generally use class method to create factory methods. Factory methods return class object
( similar to a constructor ) for different use cases.
We generally use static methods to create utility functions.

Diff:
A class method takes cls as first parameter while a static method needs no specific parameters.
A class method can access or modify class state while a static method cannot access or modify it.
In general, static methods know nothing about class state. They are utility type methods that take
 some parameters and work upon those parameters. On the other hand class methods must have class as parameter.
We use @classmethod decorator in python to create a class method and we use @staticmethod decorator
 to create a static method in python.
"""

# Python program to demonstrate
# use of class method and static method.
from datetime import date


class Person:
    color = 'red'
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # a class method to create a Person object by birth year.
    @classmethod
    def fromBirthYear(cls, name, year):
        cls.color = 'blue'
        return cls(name, date.today().year - year)

    # a static method to check if a Person is adult or not.
    @staticmethod
    def isAdult(age):
        Person.color = 'green'
        return age > 18



if __name__ == '__main__':
    person1 = Person('mayank', 21)
    person2 = Person.fromBirthYear('mayank', 1996)

    print person1.age
    print person2.age
    print person1.color
    print person2.color

    # print the result
    print Person.isAdult(22)

    print person1.color
    print person2.color