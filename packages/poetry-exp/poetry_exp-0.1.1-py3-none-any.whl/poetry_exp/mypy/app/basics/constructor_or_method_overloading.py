"""
Python's constructor: _init__ () is the first method of a class.
Whenever we try to instantiate an object __init__() is automatically invoked by
python to initialize members of an object. We can't overload constructors or methods in Python.
 It shows an error if we try to overload.
"""

class Emp:
    def __init__(self, emp_id):
        self.id = emp_id

    def __init__(self, emp_id, name):  # this will override the first definition
        self.id = emp_id
        self.name = name


def create_emp(emp_id):
    return Emp(emp_id)


def create_emp(emp_id, name):  # # this will override the first definition
    return Emp(emp_id, name)


if __name__ == '__main__':
    # e1 = Emp(1)  # TypeError: __init__() missing 1 required positional argument: 'name'
    e2 = Emp(1, 'A')

   #  e1 = create_emp(1)  # TypeError: create_emp() missing 1 required positional argument: 'name'

    e2 = create_emp(1, 'A')