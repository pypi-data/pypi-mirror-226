"""
In simple words, mutable means able to be changed and immutable
means constant
"""


def add(item, l=[]):
    l.append(item)
    return l


print add(10) # [10]
print add(20) # [10, 20]
print add(30) # [10, 20, 30] This is because default arguments defined only once

"""
List is Mutable:
Whenever you assign a variable to another
variable of mutable datatype, any changes to the data are reflected by both variables.
The new variable is just an alias for the old variable. This is only true for mutable
datatypes
"""


def add2(item, l=None):
    if l is None:
        l = list()
    l.append(item)
    return l


"""
Now whenever you call the function without the target argument, a new list is created.
"""
print add2(10) # [10]
print add2(20) # [20]
print add2(30) # [30]

"""

x = something # immutable type
print x
func(x)
print x # prints the same thing

x = something # mutable type
print x
func(x)
print x # might print something different

x = something # immutable type
y = x
print x
# some statement that operates on y
print x # prints the same thing

x = something # mutable type
y = x
print x
# some statement that operates on y
print x # might print something different

"""

x = 'foo'
y = x
print x # foo
y += 'bar'
print x # foo

x = [1, 2, 3]
y = x
print x # [1, 2, 3]
y += [3, 2, 1]
print x # [1, 2, 3, 3, 2, 1]

def func(val):
    val += 'bar'

x = 'foo'
print x # foo
func(x)
print x # foo

def func(val):
    val += [3, 2, 1]

x = [1, 2, 3]
print x # [1, 2, 3]
func(x)
print x # [1, 2, 3, 3, 2, 1]