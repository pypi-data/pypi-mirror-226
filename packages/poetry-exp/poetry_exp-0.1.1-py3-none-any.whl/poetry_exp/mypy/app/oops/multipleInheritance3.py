class A:
  def call(self):
    pass
 
class B1(A):
  def call(self):
    print "I am parent B1"
 
class B2(A):
  def call(self):
    print "I am parent B2"
 
class B3(A):
  def call(self):
    print "I am parent B3"
 
class C(A):
  def call(self):
    print "I (C) was not invited"
 
class ME(B2, B1, B3):
  def whichCall(self):
    print self.call()
 
  def restructure(self, parent1, parent2, parent3):
    self.__class__.__bases__ = (parent1, parent2, parent3, )
 
  def printBaseClasses(self):
    print self.__class__.__bases__

"""
If an object of class ME would like to call call() which one does it call,
 is it the right one, and if not, how to fix this???
The ordering of base classes defines the order of search, for an implementation of method call().
 Compare with the following example:
"""
me = ME()
 
me.printBaseClasses()
# result > (<class __main__.B2 at 0x8b1c02c>, <class __main__.B1 at 0x8b1c62c>, <class __main__.B3 at 0x8b1c05c>)
me.whichCall()
# result > I am parent B2

"""
Python allows us easily to change the order of base classes during runtime,
 and thus also the search order for the right method:
"""
me.restructure(B1, B3, B2)
me.printBaseClasses()
# result > (<class __main__.B1 at 0xa27f62c>, <class __main__.B3 at 0xa27f05c>, <class __main__.B2 at 0xa27f02c>)
me.whichCall()
# result > I am parent B1


"""
But Python allows even more. It is also possible to add parent classes (as class C),
 which was originally not defined as a parental class:
"""

me.restructure(C, B3, B2)
me.printBaseClasses()
# result > (<class __main__.C at 0xa27f08c>, <class __main__.B3 at 0xa27f05c>, <class __main__.B2 at 0xa27f02c>
me.whichCall()
# result > I (C) was not invited
