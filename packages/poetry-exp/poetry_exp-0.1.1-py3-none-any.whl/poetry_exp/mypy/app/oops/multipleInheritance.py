class A(object):
    def __init__(self):
        super(A, self).__init__()
        self.x = 10
        print "In A", self.x

    def display(self):
        print "In A", self.x


class B(A):

  def __init__(self):
    #A.__init__(self)
    super(B, self).__init__()
    print "In B, ", self.x

  def display(self):
   print "B display", self.x


class C(A):

  def __init__(self):
    #A.__init__(self)
    super(C, self).__init__()
    print "In C, ", self.x

  def display(self):
      print "C display", self.x


class D(B, C):
  def __init__(self):
    super(D, self).__init__()
    print "In D, ", self.x

  def displayD(self):
   print self.x


#b = B()
#c = C()
d = D()

d.display()


"""
In A 10
In C,  10
In B,  10
In D,  10
B display 10

"""