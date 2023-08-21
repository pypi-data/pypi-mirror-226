"""
Python doesnt restrict us from accessing any variable or calling any member method in a python program.
All python variables and methods are public by default in Python.
So when we want to make any variable or method public, we just do nothing.

When we want to declare our data member private so that nobody should be able to access it from outside the class.
Here Python supports a technique called name mangling. This feature turns every member name prefixed with at least
two underscores and suffixed with at most one underscore into _<className><memberName> .

The double underscore. It mangles the name in such a way that it cant be accessed simply through __fieldName
 from outside the class, which is what you want to begin with if they are to be private

Use single underscores for semi-private (tells python developers only change this if you absolutely must)
 and doubles for fully private


__var__: use for magic method
"""


class Test1(object):

    def __init__(this, val1, val2, val3):
        this.val1 = val1
        this._val2 = val2
        this.__val3 = val3 # will convert to _classname__variavle name

    def display(this):
        print this.val1, this._val2, this.__val3

    def _display2(this):
        print this.val1, this._val2, this.__val3

    def __display3(this):
        print this.val1, this._val2, this.__val3


if __name__ == '__main__':
    print __name__  # predefined variable when called directly has valuse as __main__
    t = Test1(10, 20, 30)
    t.display()
    t._display2()
    #t.__display3()  # cannot access this directly
    t._Test1__display3()
    print t.val1
    print t._val2
    #print t.__val3 # cannot access this directly
    print t._Test1__val3