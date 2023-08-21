"""
What is __init__.py?
It is used to import a module in a directory, which is called package import.
 If we have a module, dir1/dir2/mod.py, we put __init__.py in each directories so that we can import the mod like this:

import dir1.dir2.mod
The __init__.py is usually an empty py file. The hierarchy gives us a convenient way of organizing the files in a large system.
"""

def fun1():
  print "inside fun1"

