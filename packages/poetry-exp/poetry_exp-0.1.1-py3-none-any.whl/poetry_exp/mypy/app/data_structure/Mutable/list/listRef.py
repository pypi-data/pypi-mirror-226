def extendList(val, list=[]):
    list.append(val)
    return list


# http://www.toptal.com/python/interview-questions
list1 = extendList(10)
list2 = extendList(123,[])
list3 = extendList('a')

print "list1 = %s" % list1 #list1 =[10, 'a']
print "list2 = %s" % list2 #list2 = [123]
print "list3 = %s" % list3 #list3= [10, 'a']

print [lambda x : i * x for i in range(4)]#[<function <lambda> at 0x7f8af06dea28>, <function <lambda> at 0x7f8af06deaa0>, <function <lambda> at 0x7f8af06deb18>, <function <lambda> at 0x7f8af06deb90>]


def multipliers():
    return [lambda x : i * x for i in range(4)]


print [m(2) for m in multipliers()] #[6, 6, 6, 6]  # becomes Similar to map, applying a function to all the elements of sequence

