"""One class extending more than one class is called multiple inheritance. """

class A(object):
    def __init__(self):
        print '__init__ of A called'
        super(A, self).__init__()
        self.name = 'John'
        self.age = 23

    def getName(self):
        return self.name


class B(object):
    def __init__(self):
        print '__init__ of B called'
        super(B, self).__init__()
        self.name = 'Richard'
        self.id = '32'

    def getName(self):
        return self.name


class C(A, B):
    def __init__(self):
        print '__init__ of C called'
        super(C, self).__init__()

    def getName(self):
        return self.name


C1 = C()
print C1.name
print(C1.getName())
print C.__mro__


"""
__init__ of C called
__init__ of A called
__init__ of B called
John   # Not override by B, Richad
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <type 'object'>)


MRO works in a depth first left to right way. super() in the __init__ method indicates 
the class that is in the next hierarchy. At first the the super() of C indicates A. 
Then super in the constructor of A searches for its superclass. If it doesnot find any,
 it executes the rest of the code and returns. So the order in which constructors are called here is:
C -> A -> B
Once the constructor of A is called and attribute name is accessed, it doesnot access the 
attribute name in B. A better understanding of MRO is a must in order to work with python multiple inheritance.

"""