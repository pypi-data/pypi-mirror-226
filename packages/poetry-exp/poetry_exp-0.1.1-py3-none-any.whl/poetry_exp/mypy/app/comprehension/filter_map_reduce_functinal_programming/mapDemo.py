"""
 Python provides several functions which enable a functional approach to programming.
 Functional programming is all about expressions. We may say that the Functional programming is an expression oriented programming.

 Expression oriented functions of Python provides are:

    map(aFunction, aSequence)
    filter(aFunction, aSequence)
    reduce(aFunction, aSequence)
    lambda
    list comprehension

The map(aFunction, aSequence) function applies a passed-in function to each item in an iterable object and returns
a list containing all the function call results.
We passed in a user-defined function applied to each item in the list.
map calls sqr on each list item and collects all the return values into a new list.
Because map expects a function to be passed in, it also happens to be one of the places where lambda routinely appears:
    LIST comprehensions features were introduced in Python version 2.0, it creates a new list based on existing list.
    It maps a list into another list by applying a function to each of the elements of the existing list.
    List comprehensions creates lists without using map() , filter() or lambda form.

"""

result = map(lambda x, y: x+y, [1,2,3],[1,2,3])
print result # [2, 4, 6]

#result = map(lambda x, y: x+y, [1,2],[1,2,3]) #TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'

#result = map(lambda x, y: x+y, [1,2,3],[1,2])  # TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'

# Hence all the sequence must be of same size



def fahrenheit(T):
    return ((float(9)/5)*T + 32)


def celsius(T):
    return (float(5)/9)*(T-32)


temp = (36.5, 37, 37.5,39)
F = map(fahrenheit, temp) 

C = map(celsius, F) 
print F  # [97.7, 98.60000000000001, 99.5, 102.2]
print C  # [36.5, 37.00000000000001, 37.5, 39.0]


def sqr(x):
  return x*x

items = [1, 2, 3, 4, 5]
print map(sqr, items) #[1, 4, 9, 16, 25]
#list(map(lambda x: x*x, items)) #[1, 4, 9, 16, 25]
print items #[1, 2, 3, 4, 5]

def square(x):
        return (x**2)
def cube(x):
        return (x**3)
#we can have a list of functions as aSequence:
funcs = [square, cube]
for r in range(5):
    value = map(lambda x: x(r), funcs)
    print value

"""
[0, 0]
[1, 1]
[4, 8]
[9, 27]
[16, 64]

"""


def mymap(aFunc, aSeq):
    result = []
    for x in aSeq:
        result.append(aFunc(x))

    return result

print mymap(sqr, [1, 2, 3]) #[1, 4, 9]

"""
Since it's a built-in, map is always available and always works the same way. 
It also has some performance benefit because it is usually faster than a manually coded for loop.
On top of those, map can be used in more advance way. 
For example, given multiple sequence arguments, it sends items taken form sequences
in parallel as distinct arguments to the function:

"""
print list(map(pow,[2, 3, 4], [10, 11, 12])) #[1024, 177147, 16777216]

"""
As in the example above, with multiple sequences, map() expects an N-argument function for N sequences.
In the example, pow function takes two arguments on each call.

The map call is similar to the list comprehension expression.
But map applies a function call to each item instead of an arbitrary expression.
Because of this limitation, it is somewhat less general tool.
In some cases, however, map may be faster to run than a list comprehension such as when mapping a built-in function.
And map requires less coding.

If function is None, the identity function is assumed; 
if there are multiple arguments, map() returns a list consisting of tuples containing the
corresponding items from all iterables (a kind of transpose operation).
The iterable arguments may be a sequence or any iterable object; the result is always a list:

"""

m = [1,2,3]
n = [1,4,9]
new_tuple = map(None, m, n)
print new_tuple
# [(1, 1), (2, 4), (3, 9)]

new_tuple = map(None, n)
print new_tuple
# [1,4,9]

