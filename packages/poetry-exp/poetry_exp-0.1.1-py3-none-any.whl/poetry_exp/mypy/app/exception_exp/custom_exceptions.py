import custom_exceptions
from error_codes import ErrorCodes
import json


def load_error_messages():
    print('Loading error messages...')
    with open('error_messages.json') as f:
        return json.load(f)


ERRORS = load_error_messages()


def build_error_msg(exc):
    if isinstance(exc, custom_exceptions.CustomException):
        error_code = str(exc.error_code.value)
        error_msg = str(exc)
    else:
        error_code = str(ErrorCodes.UNKNOWN.value)
        error_msg = ERRORS[error_code]['msg'].format(*[str(exc)])

    error = dict()
    error['errors'] = ERRORS[error_code]
    error['errors']['code'] = int(error_code)
    error['errors']['msg'] = error_msg
    return error


class CustomException(Exception):
    def __init__(self, error_code, msg_args=[]):
        self.error_code = error_code
        self.msg_args = msg_args
        self.message = ERRORS[str(error_code.value)]['msg'].format(*msg_args)
        super().__init__(self.message)


class ResourceNotFound(CustomException):
    def __init__(self, msg_args=[]):
        super().__init__(ErrorCodes.NOT_FOUND, msg_args=msg_args)


class HostNotReachable(CustomException):
    pass