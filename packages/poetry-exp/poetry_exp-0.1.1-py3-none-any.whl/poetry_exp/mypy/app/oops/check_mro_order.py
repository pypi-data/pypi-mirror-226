# Following is the diamond

class A(object):
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass


if __name__ == '__main__':
    print D.__mro__

# (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <type 'object'>)
