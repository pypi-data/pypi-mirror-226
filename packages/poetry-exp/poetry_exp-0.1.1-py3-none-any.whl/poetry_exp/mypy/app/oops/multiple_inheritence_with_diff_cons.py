class A(object):
    def __init__(self, a, b):
        #super(A, self).__init__()
        print('Init {} with arguments {}'.format(self.__class__.__name__, (a, b)))

class B(object):
    def __init__(self, q):
        #super(B, self).__init__()
        print('Init {} with arguments {}'.format(self.__class__.__name__, (q)))

class C(A, B):
    def __init__(self):
        #super(C, self).__init__(1, 2)
        #super(C, self).__init__(3)

        # so here in this situation use should call init explicitly
        A.__init__(self, 1, 2)
        B.__init__(self,3)

c = C()