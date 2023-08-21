"""
The lambda operator is used to create anonymous functions.
It is mostly used in cases where one wishes to pass functions as parameters. or assign them to variable names.
Used for non reusable code
Using lambda keyword tiny anonymous functions can be created.
It is a very powerful feature of Python which declares a one-line unknown small function on the fly. The lambda is used to create new function objects and then return them at runtime.
The general format for lambda form is:
lambda parameter(s): expression using the parameter(s)
For instance k is lambda function-
>>> k= lambda y: y + y
>>> k(30)
60
>>> k(40)
80



"""

lSquare = lambda x : x*x
print "Square of 4 is ", lSquare(4)
