from enum import Enum


class StatusCodes(Enum):

    OK = '200 OK'
    NOT_FOUND = '404 Not Found'
    NOT_ALLOWED = '405 Method Not Allowed'
    FORBIDDEN = '403 Forbidden'
