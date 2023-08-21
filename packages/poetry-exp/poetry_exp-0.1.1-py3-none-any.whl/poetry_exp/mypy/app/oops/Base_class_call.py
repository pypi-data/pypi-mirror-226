"""
Base class initializer will only be called automatically if subclass initlizer is undefined
Unlike Java, Base class __init__ not called automatically if overriden
"""

class Base(object):

    def __init__(self):
        print "Base initialized"

    def fun1(self):
        print "Base fun1"


class Sub(Base):
    pass  # Will call Base Initializer automatically


class Sub2(Base):

    def __init__(self):  # Will not call Base Initializer automatically
        print 'Sub initialized'


if __name__ == '__main__':
    s = Sub() # Base initialized
    s2 = Sub2() # Sub initialized
