from datetime import datetime

from models.status_codes import StatusCodes


class Response:

    def __init__(self,
                 status_code: StatusCodes,
                 protocol: str,
                 content_type: str = None,
                 content_length: int = 0,
                 body: str = None):
        self._status_code = status_code
        self._protocol = protocol
        self._content_type = content_type
        self._content_length = content_length
        self._body = body
        self._date = datetime.utcnow()

    @property
    def status_code(self) -> StatusCodes:
        return self._status_code

    @property
    def protocol(self) -> str:
        return self._protocol

    @property
    def body(self) -> str:
        return self._body

    @property
    def content_type(self) -> str:
        return self._content_type

    @property
    def content_length(self) -> int:
        return self._content_length

    @property
    def date(self) -> datetime:
        return self._date
