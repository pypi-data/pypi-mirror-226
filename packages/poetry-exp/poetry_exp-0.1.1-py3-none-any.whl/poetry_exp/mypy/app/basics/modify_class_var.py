class Parent(object):
    x = 1

class Child1(Parent):
    pass

class Child2(Parent):
    pass

print Parent.x, Child1.x, Child2.x
#print Parent.__dict__, Child1.__dict__, Child2.__dict__

Child1.x = 2
#print Parent.__dict__, Child1.__dict__, Child2.__dict__
print Parent.x, Child1.x, Child2.x

Parent.x = 3
#print Parent.__dict__, Child1.__dict__, Child2.__dict__
print Parent.x, Child1.x, Child2.x



"""
1 1 1
1 2 1
3 2 3


What confuses or surprises many about this is that the last line of output is 3 2 3 rather than 3 2 1. 
Why does changing the value of Parent.x also change the value of Child2.x, but at the same time not change the value of Child1.x?

The key to the answer is that, in Python, class variables are internally handled as dictionaries. 
If a variable name is not found in the dictionary of the current class, the class hierarchy (i.e., its parent classes)
 are searched until the referenced variable name is found (if the referenced variable name is not found in the class 
 itself or anywhere in its hierarchy, an AttributeError occurs).

Therefore, setting x = 1 in the Parent class makes the class variable x (with a value of 1) 
referenceable in that class and any of its children. Thats why the first print statement outputs 1 1 1.

Subsequently, if any of its child classes overrides that value (for example, when we execute the statement Child1.x = 2),
 then the value is changed in that child only. Thats why the second print statement outputs 1 2 1.

Finally, if the value is then changed in the Parent (for example, when we execute the statement Parent.x = 3),
 that change is reflected also by any children that have not yet overridden the value (which in this case would be Child2).
  Thats why the third print statement outputs 3 2 3.
  
  uncomment the code and see the output
  1 1 1
{'__dict__': <attribute '__dict__' of 'Parent' objects>, 'x': 1, '__module__': '__main__', '__weakref__': <attribute '__weakref__' of 'Parent' objects>, '__doc__': None} {'__module__': '__main__', '__doc__': None} {'__module__': '__main__', '__doc__': None}
{'__dict__': <attribute '__dict__' of 'Parent' objects>, 'x': 1, '__module__': '__main__', '__weakref__': <attribute '__weakref__' of 'Parent' objects>, '__doc__': None} {'x': 2, '__module__': '__main__', '__doc__': None} {'__module__': '__main__', '__doc__': None}
1 2 1
{'__dict__': <attribute '__dict__' of 'Parent' objects>, 'x': 3, '__module__': '__main__', '__weakref__': <attribute '__weakref__' of 'Parent' objects>, '__doc__': None} {'x': 2, '__module__': '__main__', '__doc__': None} {'__module__': '__main__', '__doc__': None}
3 2 3
"""