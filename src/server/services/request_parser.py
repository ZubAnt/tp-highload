from typing import Optional

from models.request import Request


class RequestParser(object):

    def parse(self, data: str) -> Optional[Request]:
        method = self._parse_method(data)
        return None

    def _parse_method(self, data: str) -> str:
        pass
