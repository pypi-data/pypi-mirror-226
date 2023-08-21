def fun1(a, b):
    a=100
    b=200

def fun2(a, b):
    a='xyz'
    b='pqr'

def fun3(c):
    c = (100, 200)


def fun4(c, d):
    c.append(30)
    d = [100, 200]

if __name__ == '__main__':

    try:

        if '1' !=1:
            raise "SomeError"
        else:
            print 'no errr'
    except "SomeError":
        print 'some error'






    # Immuatble- int, string, touple
    x=10
    y=10
    fun1(x, y)
    print x, y  # 10, 20  Passed  by value

    x = 'abc'
    y = 'def'
    fun2(x, y)
    print x, y  # abc def  passed by value

    x = (10, 20)
    fun3(x)
    print x   # (10, 20)  Passed by value


    # Mutable - List , dict, set
    x = [10,20]
    y = [30, 40]
    fun4(x, y)
    print x, y   # [10, 20, 30] [30, 40]   Passed  by reference
