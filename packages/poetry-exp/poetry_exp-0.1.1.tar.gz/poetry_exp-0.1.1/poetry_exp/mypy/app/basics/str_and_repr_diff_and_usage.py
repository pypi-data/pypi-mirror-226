"""
str() and repr() both are used to get a string representation of object.


Following are differences:

str() is used for creating output for end user while repr() is mainly used for debugging and development.
reprs goal is to be unambiguous and strs is to be readable. For example, if we suspect a float has a small rounding error,
 repr will show us while str may not.
repr() compute the official string representation of an object (a representation that has all information about the abject)
 and str() is used to compute the informal string representation of an object (a representation that is useful
  for printing the object).


The print statement and str() built-in function uses __str__ to display the string representation of the object
 while the repr() built-in function uses __repr__ to display the object.
"""

import datetime

today = datetime.datetime.now()

# Prints readable format for date-time object
print str(today)

# prints the official format of date-time object
print repr(today)


"""
2018-07-10 22:50:20.117000
datetime.datetime(2018, 7, 10, 22, 50, 20, 117000)

str() displays todays date in a way that the user can understand the date and time.

repr() prints official representation of a date-time object 
(means using the official string representation we can reconstruct the object).
"""


# Python program to demonstrate writing of __repr__ and
# __str__ for user defined classes

# A user defined class to represent Complex numbers
class Complex:
    # Constructor
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    # For call to repr(). Prints object's information
    def __repr__(self):
        return 'Rational(%s, %s)' % (self.real, self.imag)

        # For call to str(). Prints readable form

    def __str__(self):
        return '%s + i%s' % (self.real, self.imag)


        # Driver program to test above


t = Complex(10, 20)

print str(t)  # Same as "print t"
print repr(t)


"""
10 + i20
Rational(10, 20)
"""