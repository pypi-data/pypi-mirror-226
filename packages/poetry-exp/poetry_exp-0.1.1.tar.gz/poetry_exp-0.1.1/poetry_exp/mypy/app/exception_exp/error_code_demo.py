import custom_exceptions
from custom_exceptions import build_error_msg
from error_codes import ErrorCodes
import traceback


def test1():
    try:
        raise custom_exceptions.ResourceNotFound(["123"])
    except custom_exceptions.CustomException as e:
        print('Inside CustomException: {0}'.format(e))
        return build_error_msg(e)
    except Exception as e:
        print('Inside GenericException: {0}'.format(e))
        print(traceback.format_exc())
        return build_error_msg(e)


def test2():
    try:
        raise ValueError("Invalid value")
    except custom_exceptions.CustomException as e:
        print('Inside CustomException: {0}'.format(e))
        return build_error_msg(e)
    except Exception as e:
        print('Inside GenericException: {0}'.format(e))
        print(traceback.format_exc())
        return build_error_msg(e)


def test3():
    try:
        raise custom_exceptions.HostNotReachable(ErrorCodes.HOST_NOT_REACHABLE, ["10.20.10.1"])
    except custom_exceptions.CustomException as e:
        print('Inside CustomException: {0}'.format(e))
        return build_error_msg(e)
    except Exception as e:
        print('Inside GenericException: {0}'.format(e))
        print(traceback.format_exc())
        return build_error_msg(e)


if __name__ == '__main__':

     print(test1())
     print(test2())
     print(test3())