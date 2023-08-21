class A(object): 
    def __init__(self):
        self.a = 10
        print self.a

class B(A):
    def __init__(self):
        A.__init__(self)
        self.b = 'b'
        print self.b


class C(A):
    def __init__(self):
         A.__init__(self)
         self.c = 'c'
         print self.c

class D(B,C):
    def __init__(self):
        self.d = 'd'
        print self.d
        
        super(D, self).__init__()
        print self.a

d = D()
print D.mro()


"""
d
10
b
10
[<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <type 'object'>]



"""
