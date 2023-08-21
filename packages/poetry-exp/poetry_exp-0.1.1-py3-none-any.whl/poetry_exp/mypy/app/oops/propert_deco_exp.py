"""
When a member needs to be slightly protected and cannot be simply exposed as a public member,
use Pythons property decorator to accomplish the functionality of getters and setters.
"""

class Emp(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name =value


if __name__ == '__main__':
    e = Emp("ajay")
    print e._name # ajay
    print e.name
    e.name = "aman"
    print e.name