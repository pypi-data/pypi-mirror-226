"""
The "diamond problem" (sometimes referred to as the "deadly diamond of death") is the generally used term
for an ambiguity that arises when two classes B and C inherit from a superclass A,
and another class D inherits from both B and C. If there is a method "m" in A that B or C (or even both of them) )
has overridden, and furthermore, if does not override this method,
then the question is which version of the method does D inherit? It could be the one from A, B or C

Let's look at Python. The first Diamond Problem configuration is like this: Both B and C override the method m of A:

Python solves the diamond problem with implicit behaviour mro(Method Resolution Order)
eg.
"""

class Creature:
    def cry(self):
        pass
 
class Lion(Creature):
    def cry(self):
        print("Roar!")
 
class Eagle(Creature):
    def cry(self):
        print("Emit a piercing shriek!")
 
class Griffin(Lion, Eagle):
    pass
 
g = Griffin()
g.cry()   # What gets printed?

"""
In Python, Roar gets printed. However, if we had reversed the order of the classes in the inheritance list
 (if we hadd written class Griffin(Eagle, Lion)), then Emit a piercing shriek would be printed. 
 This is because Python uses a convention called the method resolution order to figure 
 out what method to call in situations like this. 
 It basically does a breadth-first search of the inheritance graph, starting from the current class,
  then going through all the parent classes in the inheritance list (in the order they appear),
  then all of the parents parents, and so on, until it finds the method its looking for.
  In the case of the Griffin class, Python searches for an implementation of cry() in the Griffin;
  not finding one, it searches the first parent, Lion, finds the version of cry() that prints Roar,

"""


class A:
    def __init__(self):
        print 'initialized A'

    def m(self):
        print("m of A called")

class B(A):
    def __init__(self):
        print 'initialized B'

    def m(self):
        print("m of B called")
    
class C(A):
    def __init__(self):
        print 'initialized C'

    def m(self):
        print("m of C called")

class D(B,C):
    def __init__(self):
        print 'initialized D'

d = D()
d.m()

"""
initialized D
"m of B called"
If you call the method m on an instance x of D, i.e. x.m(), we will get the output "m of B called". 
If we transpose the order of the classes in the class header of D in "class D(C,B):", we will get the output "m of C called".

The case in which m will be overridden only in one of the classes B or C, e.g. in C: 
"""

class D(C,B):
    pass

d= D()
d.m()

"""
m of C called
"""


"""
The case in which m will be overridden only in one of the classes B or C, e.g. in C: 

"""
class A:  # class A(object): will give different result, i.e ....m of C called will be printed
    def m(self):
        print(".....m of A called")

class B(A):
    pass
    
class C(A):
    def m(self):
        print(".....m of C called")

class D(B,C):
    pass

x = D()

x.m()

"""
m of A called

Principially, two possibilities are imaginable: "m of C" or "m of A" could be used

We call this script with Python2.7 (python) and with Python3 (python3) to see what's happening:

$ python diamond1.py 
m of A called
$ python3 diamond1.py 
m of C called

Only for those who are interested in Python version2:
To have the same inheritance behaviour in Python2 as in Python3, every class has to inherit from the class "object".
 Our class A doesn't inherit from object, so we get a so-called old-style class, if we call the script with python2.
  Multiple inheritance with old-style classes is governed by two rules: depth-first and then left-to-right.
   If you change the header line of A into "class A(object):", we will have the same behaviour in both Python versions. 
"""


class A(object):
    def m(self):
        print("m of A called")

class B(A):
    pass
    
class C(A):
    def m(self):
        print("m of C called")

class D(B,C):
    pass

x = D()
x.m()
print D.mro()

"""
m of C called
[<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <type 'object'>]

 We have seen in our previous implementation of the diamond problem,
how Python "solves" the problem, i.e. in which order the base classes are browsed through.
The order is defined by the so-called "Method Resolution Order" or in short MRO.1\ 
"""
