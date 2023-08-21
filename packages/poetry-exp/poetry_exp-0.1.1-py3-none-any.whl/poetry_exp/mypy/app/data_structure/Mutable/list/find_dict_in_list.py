


if __name__ == '__main__':
    d1 = {"a": 1, "b": 2}
    my_list = [{"a": 1, "b": 2}, {"c": 1, "d": 2}, {"a": 4, "b": 5}]

    print d1 in my_list  # True
    print my_list.index({"c": 1, "d": 2})  # 1  Raise the value error if not found

    l1 = [1, 2, 3]
    my_list = [1, 4, 5, [1, 2, 3], 5, 6]
    print l1 in my_list  # True

    l1 = [{"a": 1}]
    my_list = [1, 4, 5, [{"a": 1}], 5, 6]
    print l1 in my_list   # True

    l1 = [1, 2, 3]
    l2 = [1, 2, 3]
    print l1 is l2  # False
    print l1 == l2  # True

    t1 = (1, 2, 3)
    t2 = (1, 2, 3)
    print t1 is t2  # False

    a = 10
    b = 10
    print a is b # True

    c = 257
    d = 257
    result = c is d  # True in shell it will be false
    """
     Python caches integers in the range [-5, 256], so it is expected that integers in that range are also identical.
    """
    print 'c is d', result
    a = 22222222222222222222222222
    b = 2222222222222222222222222
    print a is b # False

    l2 = [2, 34567788888888888888, 3, 4]
    print 34567788888888888888 in l2 # True


    print '..............Strings'

    a = 'abc'
    b = 'abc'
    print a is b # true

    a = 'zxcvbnmlkjhgfdsaqwertyuiop'
    b = 'zxcvbnmlkjhgfdsaqwertyuiop'
    print a is b # True


