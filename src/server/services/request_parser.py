from urllib import parse
from typing import Optional, Any, Dict

from models.request import Request


class RequestParser(object):

    def parse(self, data: str) -> Optional[Request]:
        method = self._parse_method(data)
        protocol = self._parse_protocol(data)
        url = self._parse_url(data)
        params = self._parse_params(data)
        headers = self._parse_headers(data)
        print(f"method: {method}")
        print(f"protocol: {protocol}")
        print(f"url: {url}")
        print(f"params: {params}")
        print(f"headers: {headers}")
        return Request(method=method, protocol=protocol, url=url, params=params, headers=headers)

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
    def _parse_url(cls, data: str) -> Optional[str]:
        try:
            print(f"[_parse_url] {(data.split(' ')[1])}")
            url = parse.unquote((data.split(' ')[1].split('?')[0]))
            # print(f"[_parse_url] url: {url}")
            # if len(url) == 0:
            #     url += '/'
            return url
        except BaseException:
            return None

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
