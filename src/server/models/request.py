from typing import Dict, Any


class Request(object):

    def __init__(self, method: str, protocol: str, url: str, headers: Dict[str, Any], params: Dict[str, Any]) -> None:
        self._method = method
        self._protocol = protocol
        self._url = url
        self._headers = headers
        self._params = params

    @property
    def method(self) -> str:
        return self._method

    @property
    def protocol(self) -> str:
        return self._protocol

    @property
    def url(self) -> str:
        return self._url

    @property
    def headers(self) -> Dict[str, Any]:
        return self._headers

    @property
    def params(self) -> Dict[str, Any]:
        return self._params
