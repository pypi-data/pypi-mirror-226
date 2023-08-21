"""
 filter extracts each element in the sequence for which the function returns True.
 The reduce function is a little less obvious in its intent. This function reduces a list to a single value by
 combining elements via a supplied function.
 The map function is the simplest one among Python built-ins used for functional programming.

These tools apply functions to sequences and other iterables.
filter filters out items based on a test function which is a filter and apply functions
to pairs of item and running result which is reduce.

Because they return iterables, range and filter both require list calls to display all their results in Python 3.0.

As an example, the following filter call picks out items in a sequence that are less than zero:

>>> list(range(-5,5))
[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
>>>
>>> list( filter((lambda x: x < 0), range(-5,5)))
[-5, -4, -3, -2, -1]
>>>


>>> l1=range(1,10)
>>> l1
[1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> l2=[10,20]
>>> x=filter(lambda x, y: x+y==4, l1,l2)  # Cann't take more than one sequence
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: filter expected 2 arguments, got 3

Items in the sequence or iterable for which the function returns a true, the result are added to the result list. Like map, this function is roughly equivalent to a for loop, but it is built-in and fast:

>>> 
>>> result = []
>>> for x in range(-5, 5):
	if x < 0:
		result.append(x)

		
>>> result
[-5, -4, -3, -2, -1]
>>> 
"""

print filter((lambda x: x<0), range(-5,5)) #[-5, -4, -3, -2, -1]

print reduce((lambda x,y:x+y), [1,2,3,4])#10  1+2 = 3, 3+3=6, 6+4=10

"""
The reduce is in the functools in Python 3.0. It is more complex. It accepts an iterator to process,
 but it's not an iterator itself. It returns a single result:

>>> 
>>> from functools import reduce
>>> reduce( (lambda x, y: x * y), [1, 2, 3, 4] )
24
>>> reduce( (lambda x, y: x / y), [1, 2, 3, 4] )
0.041666666666666664
>>> 

At each step, reduce passes the current product or division, along with the next item from the list, to the passed-in lambda function. By default, the first item in the sequence initialized the starting value.

Here's the for loop version of the first of these calls, with the multiplication hardcoded inside the loop:

>>> L = [1, 2, 3, 4]
>>> result = L[0]
>>> for x in L[1:]:
	result = result * x

	
>>> result
24
>>> 

Let's make our own version of reduce.

>>> def myreduce(fnc, seq):
	tally = seq[0]
	for next in seq[1:]:
		tally = fnc(tally, next)
	return tally

>>> myreduce( (lambda x, y: x * y), [1, 2, 3, 4])
24
>>> myreduce( (lambda x, y: x / y), [1, 2, 3, 4])
0.041666666666666664
>>> 


We can concatenate a list of strings to make a sentence. Using the Dijkstra's famous quote on bug:

import functools
>>> L = ['Testing ', 'shows ', 'the ', 'presence', ', ','not ', 'the ', 'absence ', 'of ', 'bugs']
>>> functools.reduce( (lambda x,y:x+y), L)
'Testing shows the presence, not the absence of bugs'
>>> 

We can get the same result by using join :

>>> ''.join(L)
'Testing shows the presence, not the absence of bugs'

We can also use operator to produce the same result:

>>> import functools, operator
>>> functools.reduce(operator.add, L)
'Testing shows the presence, not the absence of bugs'
>>> 

The built-in reduce also allows an optional third argument placed before the items in the sequence to serve as a default result when the sequence is empty."""

