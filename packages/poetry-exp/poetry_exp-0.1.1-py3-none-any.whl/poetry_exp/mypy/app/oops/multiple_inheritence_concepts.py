"""
- If a class has multiple base class and no init defined,
    then only the init of the first base class will be called automatically


MRO(Method Resolution Order): determines the ordering of method lookup,
    - When you call the method on object, then it first search that method in the same class
      if not found search it in the parent classes from left to right order and then start search in Parent's Parent

    - Python uses C3 algo for calculating MRO
       - subclasses comes before base classes
       - Base classes order from class definition is preserved
       - first two quality are preserved no matter from where you start in inheritance graph
       -
"""


class Parent(object):
    pass


class Base1(Parent):

    def __init__(self):
        print "Base1 Initializer"


class Base2(Parent):
    def __init__(self):
        print "Base2 Initializer"


class Sub(Base1, Base2):
    pass


class Sub2(Base1, Base2, Parent):
    pass


#class Sub3(Base1, Parent, Base2):  # Cannot create a consistent method resolution order (MRO) for bases Base2, Parent
#    pass



if __name__=='__main__':

    s = Sub() # Base1 Initializer

    print Sub.__bases__  # (<class '__main__.Base1'>, <class '__main__.Base2'>)
    print Sub.__mro__ # (<class '__main__.Sub'>, <class '__main__.Base1'>, <class '__main__.Base2'>, <class '__main__.Parent'>, <type 'object'>)


