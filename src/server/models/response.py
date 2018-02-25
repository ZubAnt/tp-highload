from datetime import datetime

from models.status_codes import StatusCodes


class Response:
    def __init__(self, code: StatusCodes, protocol: str, content_type: str = None,
                 content_length: int = 0,
                 data = b''):
        self._status_code = code
        self._protocol = protocol
        self._data = data
        self._content_type = content_type
        self._content_length = content_length
        self._date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

    def _success(self):
        return 'HTTP/{} {}\r\n' \
               'Content-Type: {}\r\n' \
               'Content-Length: {}\r\n'\
               'Date: {}\r\n' \
               'Server: Server\r\n\r\n'.format(self._protocol,
                                               self._status_code.value,
                                               self._content_type,
                                               self._content_length,
                                               self._date)

    def _error(self):
        return 'HTTP/{} {}\r\n' \
               'Server: Server'.format(self._protocol, self._status_code.value)

    def dump(self):
        if self._status_code == StatusCodes.OK:
            return self._success().encode() + self._data
        if self._status_code == StatusCodes.NOT_FOUND \
                or self._status_code == StatusCodes.NOT_ALLOWED \
                or self._status_code == StatusCodes.FORBIDDEN:
            return self._error().encode()