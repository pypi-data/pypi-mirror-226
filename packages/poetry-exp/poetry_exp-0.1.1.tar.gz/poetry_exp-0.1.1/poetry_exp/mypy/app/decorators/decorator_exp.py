"""
A callable used to transform a function, method or class object.
"""

def log_result2(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print 'Inside 2, Function {0} called with args: {1} and kwargs: {2}, result: {3}'.format(
            func.__name__, args, kwargs, result)
        return result
    return wrapper

def log_result(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print 'Inside1, Function {0} called with args: {1} and kwargs: {2}, result: {3}'.format(
            func.__name__, args, kwargs, result)
        return result
    return wrapper


def sub(a, b=0):
    return a-b


# Another way of calling decorator,
#  @ is just a short way of making up a decorated function, but it will change the func name and doc string
minus = log_result(sub)
minus(20, 10)

print sub.__name__ # sub

@log_result2   # then this will execute
@log_result    # First this will execute
def add(a, b=10):
    return a+b


add(10, 10)
print add.__name__  #  wrapper, to avoid this use functools wrap decorator in your decorator


from functools import wraps


def log_result2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print 'Function {0} called with args: {1} and kwargs: {2}, result: {3}'.format(
            func.__name__, args, kwargs, result)
        return result
    return wrapper

"""
@ wraps takes a function to be decorated and adds the functionality of copying
over the function name, docstring, arguments list, etc. This allows to access the predecorated
function properties in the decorator.
"""

@log_result2
def mul(a, b=1):
    return a*b


mul(10)
mul(10, b=90)
print mul.__name__  # mul


"""
Usage of decorator:
Authorization, logging
Decorators can help to check whether someone is authorized to use an endpoint in a
web application. They are extensively used in Flask web framework and Django. Here
is an example to employ decorator based authentication:
Example :

from functools import wraps
from requests import request
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            authenticate()
        return f(*args, **kwargs)
    return decorated
"""


# Decorator with args
def logit(log_file='out.log'):
    def log_decorator(func, *args, **kwargs):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            log_string = '\nFunction {0} called with args: {1} and kwargs: {2}, result: {3}'.format(
                func.__name__, args, kwargs, result)
            print log_string
            with open(log_file, 'a') as f:
                f.write(log_string)
            return result
        return wrapper
    return log_decorator

@logit(log_file='test.log')
def divide(a, b):
    return a/b

divide(10,5)

print divide.__name__

