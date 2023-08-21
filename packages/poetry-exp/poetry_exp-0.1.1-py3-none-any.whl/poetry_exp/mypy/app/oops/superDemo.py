class A(object):

  def __init__(self, x):
     self.x=x

  def display(self):
   print "x=",self.x

class B(A):
  def __init__(self,y):
   super(B, self).__init__(y)

   # OR
   #A.__init__(self, y)
   self.y = y

b= B(12)
b.display()

