try:
    a = 10/0
except (ZeroDivisionError, Exception) as e:
    print(f'Error: {str(e)}, Type: {type(e)}')

try:
    a = 10/0
    d = {"a": 1}
    print(d["b"])
except (Exception, ZeroDivisionError) as e:
    print(f'Error: {str(e)}, Type: {type(e)}')
    if isinstance(e, ZeroDivisionError):
        print(f'Divide by zero: {e}')
    elif isinstance(e, KeyError):
        print(f'Key error exception: {e}')
    else:
        print(f'Generic exception: {e}')

"""
OUTPUT:
Error: division by zero, Type: <class 'ZeroDivisionError'>
Error: division by zero, Type: <class 'ZeroDivisionError'>
"""