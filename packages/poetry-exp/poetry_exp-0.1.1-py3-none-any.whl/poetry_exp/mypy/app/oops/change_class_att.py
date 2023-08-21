class C:
    dangerous = 2  # Class attr


c1 = C()
c2 = C()

print c1.dangerous # 2

c1.dangerous = 3  # changes in the object will not affect other object and class
print c1.dangerous, c2.dangerous  # 3 2

del c1.dangerous  # delete the object copy
print c1.dangerous  # 2

C.dangerous = 3
print c2.dangerous  # 3


class D:
    dan = 1

d1 = D()
d2 = D()

print d1.dan # 1
print d2.dan # 1

D.dan = 2  # Change in class will affect existing and new objects

d3 = D()
print d1.dan, d2.dan, d3.dan  # 2 2 2


class E:
    dan = 1

e = E()
print e.dan # 1

#del e.dan  # error: AttributeError: E instance has no attribute 'dan'

e.dan=2  # This is object's personal
print e.dan # 2

del e.dan  # deleted the object's attr not class one

print e.dan  # 1