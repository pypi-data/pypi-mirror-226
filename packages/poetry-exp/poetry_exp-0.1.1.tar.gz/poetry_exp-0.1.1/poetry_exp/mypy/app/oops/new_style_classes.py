"""

New style classes were introduced in Python 2.1 but a lot of people do not know about
them even now! It is so because Python also supports old style classes just to maintain
backward compatibility. I have said a lot about new and old but I have not told you
about the difference. Well the major difference is that:
- Old base classes do not inherit from anything
- New style base classes inherit from object
A very basic example is:

This inheritance from object allows new style classes to utilize some magic. A major
advantage is that you can employ some useful optimizations like __slots__. You can
use super() and descriptors and the likes. Bottom line? Always try to use new-style
classes.
Note: Python 3 only has new-style classes. It does not matter whether you subclass
from object or not. However it is recommended that you still subclass from object.
"""


class OldClass:
    def __init__(self):
        print('I am an old class')


class NewClass(object):
    def __init__(self):
        print('I am a jazzy new class')

old = OldClass() # Output: I am an old class
new = NewClass() # Output: I am a jazzy new class
