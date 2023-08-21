def fun1(a, b):
    a += 100
    b += 200
#  Local Variables: If a variable is assigned a new value anywhere within the function's body, it's assumed to be local.
# Global variables: Those variables that are only referenced inside a function are implicitly global.



def fun2(a, b):
    a = 'xyz'
    b = 'pqr'


def fun3(c):
    c = (100, 200)


def fun4(c, d):
    c.append(30) # changing c
    d = [100, 200] # now d becomes local, will not change d


if __name__ == '__main__':
    # Immuatble- int, string, touple
    x = 10
    y = 10
    fun1(x, y)
    print x, y  # 10, 10  Passed  by value

    x = 'abc'
    y = 'def'
    fun2(x, y)
    print x, y  # abc def  passed by value

    x = (10, 20)
    fun3(x)
    print x  # (10, 20)

    # Mutable - List , dict, set
    x = [10, 20]
    y = [30, 40]
    fun4(x, y)
    print x, y  # [10, 20, 30] [30, 40]   Passed  by reference
