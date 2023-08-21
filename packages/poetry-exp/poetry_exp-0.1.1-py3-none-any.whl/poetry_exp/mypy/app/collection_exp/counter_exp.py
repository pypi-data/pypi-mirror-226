"""
Counter allows us to count the occurrences of a particular item
"""

from collections import Counter
# aafak
value_counter = Counter([10, 20, 30, 10, 20, 10])
print value_counter # Counter({10: 3, 20: 2, 30: 1})
print type(value_counter) # <class 'collections.Counter'>
print value_counter.items() # [(10, 3), (20, 2), (30, 1)]
for k, v in value_counter.items():
    print k, "comes", v, "times"

# aafak
with open("counter_exp.py", 'rb') as f:
    line_count = Counter(f)

print line_count  # Tells which line

"""
Counter({'# aafak\r\n': 2, '\r\n': 2, 'for k, v in value_counter.items():\r\n': 1,
 'from collections import  Counter\r\n': 1, 'value_counter = Counter([10, 20, 30, 10, 20, 10])\r\n': 1,
  "print type(value_counter) # <class 'collections.Counter'>\r\n": 1, 'print line_count': 1, '
      print k, "comes", v, "times"\r\n': 1, 'with open("counter_exp.py", \'rb\') as f:\r\n': 1, '
          line_count = Counter(f)\r\n': 1, 'print value_counter.items() # [(10, 3), (20, 2), (30, 1)]\r\n': 1,
           'print value_counter # Counter({10: 3, 20: 2, 30: 1})\r\n': 1})

"""