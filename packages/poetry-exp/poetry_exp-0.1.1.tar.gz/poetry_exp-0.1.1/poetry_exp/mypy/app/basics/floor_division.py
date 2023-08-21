def div1(x, y):
    print "%s/%s = %s" % (x, y, x / y)


def div2(x, y):
    print "%s//%s = %s" % (x, y, x // y)


div1(5, 2)
div1(5., 2)
div2(5, 2)
div2(5., 2.)

"""
In Python2,
By default, Python 2 automatically performs integer arithmetic if both operands are integers
5/2 = 2
5.0/2 = 2.5
5//2 = 2
5.0//2.0 = 2.0

double-slash (//) operator will always perform integer division, regardless of the operand types,
it basically cuts of the part after the period


In Python3,
Python 3, however, does not have this behavior; i.e., 
it does not perform integer arithmetic if both operands are integers. 
Therefore, in Python 3, the output will be as follows
5/2 = 2.5
5.0/2 = 2.5
5//2 = 2
5.0//2.0 = 2.0
"""