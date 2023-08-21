d = {}
class CustomException(Exception):
    pass


c1 = CustomException("Hello exception")
e1 = Exception('Hi Exception')
print isinstance(e1, Exception)  # True
print isinstance(c1, Exception)  # True

print type(e1) is Exception  # True
print type(c1) is Exception  # False
try:
    print d['snapshot']
except Exception as e:
    if hasattr(e, "msg"):
        msg = e.msg
    elif hasattr(e, "message"):
        msg = e.message
        if isinstance(e, Exception):
            msg = 'Unknown error'
            print 'comes here..'
    else:
        msg = "Internal error"

    print msg