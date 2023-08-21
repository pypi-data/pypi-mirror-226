"""
- Generators are a special kind of function, which enable us to implement or generate iterators.
- A generator is a function which returns a generator object. This generator object can be seen like a
  function which produces a sequence of results instead of a single object. This sequence of values is produced
  by iterating over it, e.g. with a for loop.

- Everything which can be done with a generator can also be implemented with a class based iterator as well.
  But the crucial advantage of generators consists in automatically creating the methods __iter__() and next().
  Generators provide a very neat way of producing data which is huge or infinite
- The generators offer a comfortable method to generate iterators, and that's why they are called generators.


>>> l = [i for i in range(10)]
>>> l
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> l = (i for i in range(10))
>>> l
<generator object <genexpr> at 0x0000013C688A0F10>
>>>

a generator looks like a function but behaves like an iterator, generates a sequence of values
A generator yields the values one at a time, which requires less memory and allows the caller to get started processing the first few values immediately.
A generator function is a way to create an iterator. A new generator object is created and returned each time we call a generator function.


The yield enables a function to comeback where it left off when it is called again. This is the critical difference from a regular function. A regular function cannot comes back where it left off. The yield keyword helps a function to remember its state.
a generator is a special routine that can be used to control the iteration behavior of a loop.

Python provides tools that produce results only when needed:

    1. Generator functions:
    They are coded as normal def but use yield to return results one at a time, suspending and resuming.
				def create_counter(n):
						print('create_counter()')
						while True:
							yield n
							print('increment n')
							n += 1
		
					>>> c = create_counter(2)
					>>> c
					<generator object create_counter at 0x03004B48>
					>>> next(c)
					create_counter()
					2
					>>> next(c)
					increment n
					3
					>>> next(c)
					increment n
					4
					>>> 

    2. Generator expressions:
    These are similar to the list comprehensions. But they return an object that produces results on demand instead of building a result list.
      and they are enclosed in parentheses
     >>> # List comprehension makes a list
					>>> [ x ** 3 for x in range(5)]
					[0, 1, 8, 27, 64]
					>>> 
					>>> # Generator expression makes an iterable
					>>> (x ** 3 for x in range(5))
					<generator object <genexpr> at 0x000000000315F678>
					>>> 

				>>> Generator = (x ** 3 for x in range(5))
				>>> next(Generator)
				0
				>>> next(Generator)
				1
				>>> next(Generator)
				8
				>>> next(Generator)
				27
				>>> next(Generator)
				64
				>>> next(Generator)
				Traceback (most recent call last):
						File "<pyshell#68>", line 1, in <module>
								next(Generator)
				StopIteration
				>>> 

Because neither of them constructs a result list all at once, they save memory space and allow computation time to be split by implementing the iteration protocol.

The primary difference between generator and normal functions is that a generator yields a value, rather than returns a value. The yield suspends the function and sends a value back to the caller while retains enough state to enable the function immediately after the last yield run. This allows the generator function to produce a series of values over time rather than computing them all at once and sending them back in a list.

>>> def create_counter(n):
	print('create_counter()')
	while True:
		yield n
		print('increment n')
		n += 1
		
>>> c = create_counter(2)
>>> c
<generator object create_counter at 0x03004B48>
>>> next(c)
create_counter()
2
>>> next(c)
increment n
3
>>> next(c)
increment n
4
>>> 

Here are the things happening in the code:

    The presence of the yield keyword in create_counter() means that this is not a normal function. It is a special kind of function which generates values one at a time. We can think of it as a resumable function. Calling it will return a generator that can be used to generate successive values of n.
    To create an instance of the create_counter() generator, just call it like any other function. Note that this does not actually execute the function code. We can tell this because the first line of the create_counter() function calls print(), but nothing was printed from the line:

    >>> c = create_counter(2)

    The create_counter() function returns a generator object.
    The next() function takes a generator object and returns its next value. The first time we call next() with the counter generator, it executes the code in create_counter() up to the first yield statement, then returns the value that was yielded. In this case, that will be 2, because we originally created the generator by calling create_counter(2).
    Repeatedly calling next() with the same generator object resumes exactly where it left off and continues until it hits the next yield statement. All variables, local state, &c. are saved on yield and restored on next(). The next line of code waiting to be executed calls print(), which prints increment n. After that, the statement n += 1. Then it loops through the while loop again, and the first thing it hits is the statement yield n, which saves the state of everything and returns the current value of n (now 3).
    The second time we call next(c), we do all the same things again, but this time n is now 4.
    Since create_counter() sets up an infinite loop, we could theoretically do this forever, and it would just keep incrementing n and spitting out values.
"""

def f(n): 
    print ("starting...") #execute only once
    for x in range(n):
        yield x**3#x to the power 3

    print ("end")#execute only once

for x in f(5):
    print (x) #0,1,8,27,64

def isPrime(n):
  """ Prime number is a positive natural number that has only two positive natural number divisors - one and itself.
      The opposite of prime numbers are composite numbers. A composite number is a positive nutural number that has at least one 
      positive divisor other than one or itself.
      The number 1 is not a prime number by definition - it has only one divisor.
      The number 0 is not a prime number - it is not a positive number and has infinite number of divisors.
      The number 2 is a prime number. Two has 2 natural number divisors - 1 and 2:
  """

  if n==0 or n==1:
    return False

  for i in range(2,n): #For n=2 it will not execute
    if n%i == 0:
       return False
  return True

print (isPrime(2)) #True


def primes(n=1):
   while n<100:
      if isPrime(n):
          yield n  # yields n instead of returns n
      n+=1# next call it will increment n by 1

print ("Prime numbers")
for n in primes(10):
  print (n)


#Generate 10 fib number
def fibonacci1(limit=10):
  a,b = 0,1
  count = 0
  while True:
    yield a
    if count == limit:
       break;
    a,b = b, a+b
    count+=1

#Generate fib number up to 10
def fibonacci2(max=10):
   a, b = 0, 1            
   while a < max:
       yield a            
       a, b = b, a + b  


for n in fibonacci1():
  print (n) #0 1 1 2 3 5 8 13 21 34 55

print ("\nfib ver2")

for n in fibonacci2():
  print (n) #0 1 1 2 3 5 8
"""
The for loop will automatically call the next() function to get values from the fibonacci() generator and 
assign them to the for loop index variable (n)
"""
     




