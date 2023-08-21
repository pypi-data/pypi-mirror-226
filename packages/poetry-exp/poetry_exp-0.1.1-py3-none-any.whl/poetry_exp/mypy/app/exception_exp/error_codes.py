from enum import Enum


class ErrorCodes(Enum):
    NOT_FOUND = 404
    UNKNOWN = 500
    HOST_NOT_REACHABLE = 499