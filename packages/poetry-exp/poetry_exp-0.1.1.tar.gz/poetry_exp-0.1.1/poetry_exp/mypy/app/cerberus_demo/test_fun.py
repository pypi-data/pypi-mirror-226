def fun1(abc=[]):
    abc['a'] = 1
    return abc


abc = {}
result  = fun1(abc=abc)
print abc