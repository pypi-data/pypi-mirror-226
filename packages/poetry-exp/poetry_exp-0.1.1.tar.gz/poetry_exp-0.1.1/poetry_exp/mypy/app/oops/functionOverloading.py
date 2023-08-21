#Python does not support function overloading

def f1(a, b):
  print 'I am at top'


def f1(a):
  print 'I am at bottom'


f1(10) # I am at bottom
# f1(10, 20) # Error TypeError: f1() takes exactly 1 argument (2 given)

def fun1(a,b):
  print "a=%s, b=%s" %(a,b)

def fun1(a): #Latest defination for fun1, now no more fun1(a,b) exists
  print "a=%s" %(a,) 

fun1(10)
fun1(10,20) #TypeError: fun1() takes exactly 1 argument (2 given)

