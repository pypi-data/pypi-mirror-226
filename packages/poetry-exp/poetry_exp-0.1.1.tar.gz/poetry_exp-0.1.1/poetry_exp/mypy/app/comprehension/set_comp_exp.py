"""
They are also similar to list comprehensions. The only difference is that they use curly braces
{}
"""

numbers = range(30)
odd_numbers = {n for n in numbers if n%2 == 1}
print odd_numbers # set([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29])


