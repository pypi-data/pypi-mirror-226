"""

 Function Argument Unpacking is another awesome feature of Python.
 One can unpack a list or a dictionary as function arguments using * and ** respectively.
 This is commonly known as the Splat operator
"""

def point(x, y):
    print(x, y)


foo_list = (3, 4)
bar_dict = {'y': 3, 'x': 2}

point(*foo_list)  # Unpacking Lists
point(**bar_dict)  # Unpacking Dictionaries