"""
There are two parameters passing mechanism in Python:

Pass by references
Pass by value
By default, all the parameters (arguments) are passed "by reference" to the functions. (looks wrong)
Thus, if you change the value of the parameter within a function, the change is reflected in
the calling function as well. It indicates the original variable. For example, if a variable
is declared as a = 10, and passed to a function where it's value is modified to a = 20.
Both the variables denote to the same value.

The pass by value is that whenever we pass the arguments to the function only values pass to the function,
no reference passes to the function. It makes it immutable that means not changeable.
Both variables hold the different values, and original value persists even after modifying in the function.


Python has a default argument concept which helps to call a method using an arbitrary number of arguments.

"""

def greet(name):
    name = "Welcome " + name
    print(name)


def print_salary(salary):
    salary = 500
    print(salary)


def print_users(users):
    users.append('C')
    print(users)

if __name__ == '__main__':
    user_name = "John"
    greet(user_name)  # pass by value
    print(user_name)
    sal = 100
    print_salary(sal)  # pass by value
    print(sal)  # 100, not modified

    users = ['A', 'B']
    print_users(users)  # pass by reference
    print(users)    # ['A', 'B', 'C']  Modified by method
