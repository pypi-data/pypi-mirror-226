"""
 Python provides several functions which enable a functional approach to programming.
 Functional programming is all about expressions. We may say that the Functional programming is an expression oriented programming.

 Expression oriented functions of Python provides are:

    map(aFunction, aSequence)
    filter(aFunction, aSequence)
    reduce(aFunction, aSequence)
    lambda
    list comprehension

 List comprehension is an elegant way to define and create list in Python
 LIST comprehensions features were introduced in Python version 2.0, it creates a new list based on existing list.
    It maps a list into another list by applying a function to each of the elements of the existing list.
    List comprehensions creates lists without using map() , filter() or lambda form.
List comprehension is a complete substitute for the lambda function as well as the functions map(), filter() and reduce()

list comprehension
>>> list([x**2 for x in range(4)])
[0, 1, 4, 9]
Generator expression
>>> (x**2 for x in range(4))
<generator object <genexpr> at 0x7f60583dc960>
>>> 
>>> Generator = (x ** 3 for x in range(5))
>>> next(Generator)
0
>>> next(Generator)

Generator expressions are a memory-space optimization. They do not require the entire result list to be
constructed all at once while the square-bracketed list comprehension does.
They may also run slightly slower in practice, so they are probably best used only for very large result sets.

>> [(x,y,z) for x in range(1,30) for y in range(x,30) for z in range(y,30) if x**2 + y**2 == z**2]
[(3, 4, 5), (5, 12, 13), (6, 8, 10), (7, 24, 25), (8, 15, 17), (9, 12, 15), (10, 24, 26), (12, 16, 20), (15, 20, 25), (20, 21, 29)]
>>> 


Cross product of two sets:

>>> colours = [ "red", "green", "yellow", "blue" ]
>>> things = [ "house", "car", "tree" ]
>>> coloured_things = [ (x,y) for x in colours for y in things ]
>>> print coloured_things
[('red', 'house'), ('red', 'car'), ('red', 'tree'), ('green', 'house'), ('green', 'car'), ('green', 'tree'), ('yellow', 'house'), ('yellow', 'car'), ('yellow', 'tree'), ('blue', 'house'), ('blue', 'car'), ('blue', 'tree')]
>>> 

Generator comprehensions were introduced with Python 2.6. They are simply a generator expression with a parenthesis - round brackets - around it. Otherwise, the syntax and the way of working is like list comprehension, but a generator comprehension returns a generator instead of a list.

>>> x = (x **2 for x in range(20))
>>> print(x)
 at 0xb7307aa4>
>>> x = list(x)
>>> print(x)
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361]

A more Demanding Example
Calculation of the prime numbers between 1 and 100 using the sieve of Eratosthenes:

>>> noprimes = [j for i in range(2, 8) for j in range(i*2, 100, i)]
>>> primes = [x for x in range(2, 100) if x not in noprimes]
>>> print primes
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
>>> 

We want to bring the previous example into more general form, so that we can calculate the list of prime numbers up to an arbitrary number n:

>>> from math import sqrt
>>> n = 100
>>> sqrt_n = int(sqrt(n))
>>> no_primes = [j for i in range(2,sqrt_n) for j in range(i*2, n, i)]

If we have a look at the content of no_primes, we can see that we have a problem. There are lots of double entries contained in this list:

>>> no_primes
[4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92, 96, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 18, 27, 36, 45, 54, 63, 72, 81, 90, 99]
>>>

"""

Celsius = [39.2, 36.5, 37.3, 37.8]
Fahrenheit = [ ((float(9)/5)*x + 32) for x in Celsius ] #subsitute for map
print Fahrenheit
#[102.56, 97.700000000000003, 99.140000000000001, 100.03999999999999]

list1 =  [-5, -4, -3, -2, -1, 0,1,2,3,4,5]
print filter((lambda x: x<0), list1) #[-5, -4, -3, -2, -1]

print [x for x in list1 if x<0] #[-5, -4, -3, -2, -1] #subsitute for filter



