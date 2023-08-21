
"""
Comprehensions are constructs that allow sequences to be built from other
sequences. Three types of comprehensions are supported in both Python 2 and Python
3:
 - list comprehensions
 - dictionary comprehensions
 - set comprehensions
 - generator comprehensions

"""

numbers = range(30)
even_numbers = [n for n in numbers if n%2==0]
print even_numbers #[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
# This is equal to filter function

num_squers = [n**2 for n in numbers]
print num_squers  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400, 441, 484, 529, 576, 625, 676, 729, 784, 841]
# This is equivalant to map function