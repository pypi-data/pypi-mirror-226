"""
The yield enables a function to comeback where it left off when it is called again.
 This is the critical difference from a regular function.
 A regular function cannot comes back where it left off. The yield keyword helps a function to remember its state.

Let's look at the following sample code which has 3 yields and it is iterated over 3 times, and each time it comes back to the next execution line in the function not starting from the beginning of the function body:

Simply put, the yield enables a function to suspend and resume while it turns in a value at the time of the suspension of the execution.
"""

def foo_with_yield():
    print "Start..."#execute only once
    yield 1
    yield 2
    yield 3
    print "End"#execute only once

# iterative calls
for yield_value in foo_with_yield():
    print yield_value, #1 2 3  , for not going to next line


#what actually generator object returns 
x=foo_with_yield()
print x #<generator object foo_with_yield at 0x7f6e4f0f1e60>
print next(x)#1
print x#<generator object foo_with_yield at 0x7f6e4f0f1e60>
print next(x)#2
print x#<generator object foo_with_yield at 0x7f6e4f0f1e60>
print next(x)#3

"""
The next() function takes a generator object and returns its next value. Repeatedly calling next() with the same generator object resumes exactly where it left off and continues until it hits the next yield statement. All variables and local state are saved on yield and restored on next(). """


"""
What does for-loop do with the generator object?

Generators are closely tied with the iteration protocol. Iterable objects define a __next__() method which either returns 
the next item in the iterator or raises the special StopIteration exception to end the iteration. 
An object's iterator is fetched with the iter built-in function.

The for loops use this iteration protocol to step through a sequence or value generator if the protocol is suspended. 
Otherwise, iteration falls back on repeatedly indexing sequences.

To support this protocol, functions with yield statement are compiled specially as generators.
 They return a generator object when they are called. The returned object supports the iteration interface 
 with an automatically created __next__() method to resume execution.
  Generator functions may have a return simply terminates the generation of values by
   raising a StopIteration exceptions after any normal function exit.

The net effect is that generator functions, coded as def statements containing yield statement, are automatically made to
 support the iteration protocol and thus may be used any iteration context to produce results over time and on demand.

In short, a generator looks like a function but behaves like an iterator.

"""


