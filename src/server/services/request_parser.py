from urllib import parse
from urllib.parse import urlparse, ParseResult
from typing import Optional, Any, Dict

from models.request import Request


class RequestParser(object):

    def parse(self, data: str) -> Optional[Request]:
        method = self._parse_method(data)
        protocol = self._parse_protocol(data)

        res: ParseResult = self._parse_url(data)

        if not res:
            path = None
            params = None
        else:
            path = self._convert_path(res.path)
            params = self._convert_params(res.params)

        headers = self._parse_headers(data)
        return Request(method=method, protocol=protocol, path=path, params=params, headers=headers)

    @classmethod
    def _parse_method(cls, data: str) -> str:
        return data.split(' ')[0]

    @classmethod
    def _parse_protocol(cls, data: str):
        try:
            return data.split('\r\n')[0].split(' ')[2].split('HTTP/')[1]
        except IndexError:
            return '1.0'

    @classmethod
    def _convert_path(cls, path: str) -> str:
        return parse.unquote(path)

    @classmethod
    def _convert_params(cls, params: str) -> Optional[Dict[str, Any]]:
        data = {}
        try:
            for param in params:
                key, val = param.split('=')
                data.update({key: val})
            return data
        except ValueError:
            return None
        except IndexError:
            return None

    @classmethod
    def _get_url(cls, data: str) -> Optional[str]:
        try:
            return data.split(' ')[1].split('?')[0]
        except IndexError:
            return None

    @classmethod
    def _parse_url(cls, data: str) -> Optional[ParseResult]:
        url = cls._get_url(data)
        return None if url is None else urlparse(url)

    @classmethod
    def _parse_params(cls, data: str) -> Optional[Dict[str, Any]]:
        params = {}
        try:
            for param in data.split(' ')[1].split('?')[1].split('&'):
                key, val = param.split('=')
                params.update({key: val})
            return params
        except ValueError:
            return None
        except IndexError:
            return None

    @classmethod
    def _parse_headers(cls, data: str) -> Optional[Dict[str, Any]]:
        headers = {}

        try:
            for header in data.split('\r\n\r\n')[0].split('\r\n')[1:]:
                headers[header.split(':')[0]] = header.split(':')[1][1:]
            return headers
        except IndexError:
            return None
