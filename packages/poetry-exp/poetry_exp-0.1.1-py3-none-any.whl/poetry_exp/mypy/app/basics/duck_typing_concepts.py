"""
Duck Typing:
This is a feature of dynamic languages. This is duck typing.
The idea is that it doesnt actually matter what type my data is - just whether or not I can do what I want with it.


Duck typing is a concept that says that the type of the object is a matter of concern 
only at runtime and you dont need to to explicitly mention the type of the object before 
you perform nay kind of operation on that object.

The following example can help in understanding this concept -

def calc(a,b): 
 return a+b
 
Now, Python says that for the above function I dont need to be concerned about the type of the objects a & b
 and that the type will be taken care of during runtime as long as the objects support the + .
  So, keeping this in mind the above function will work for any type of object which supports the operator + i.e.
   it will return valid values for a string, list or Integer. When I pass the following types of object then the function should work-

calc(1,2) → will return 1+2 = 3 
calc(hello, world) --> will return hello world
calc([1],[2]) --> will return [1,2]
What we got in the above results?

In the first example of 1,2 since python interpreter recognizes these objects as type integer and since the operator
 + is valid for integers so the function calc returns a valid output of type integer 3.
  Here while passing the objects 1,2 to the function calc we are not defining that these objects are type
   integer as due to duck typing concept in python, the objects 1,2 are interpreted as integers and hence the function calc must return a output of type integer.
In the second example we did not explicitly mentioned anywhere that the objects hello & world are of type string, but duck typing concept comes into play and the interpreter recognizes these objects as strings during runtime and when these are passed to the function calc then the output should be a valid string ‘hello world’.

"""