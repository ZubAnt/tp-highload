import os

from asyncio import AbstractEventLoop
from typing import Optional

from configs.configure import Configure
from models.content_types import ContentTypes
from models.request import Request
from models.resource import Resource
from models.response import Response
from models.status_codes import StatusCodes
from services.file_reader import FileReader


class ForbiddenError(BaseException):
    pass


class NotFoundError(BaseException):
    pass


class RequestExecutor(object):

    def __init__(self, conf: Configure, loop: AbstractEventLoop) -> None:
        self._conf = conf
        self._loop = loop
        self._reader = FileReader(conf, loop)

    async def execute(self, request: Request) -> Optional[Response]:
        if request.method not in ('GET', 'HEAD'):
            return Response(status_code=StatusCodes.NOT_ALLOWED, protocol=request.protocol)

        if request.method == 'HEAD':
            return await self._execute_head_request(request=request)

        elif request.method == 'GET':
            return await self._execute_get_request(request=request)

    async def _execute_head_request(self, request: Request) -> Response:
        try:
            resource = self._build_resource(request)
        except ForbiddenError:
            return Response(status_code=StatusCodes.FORBIDDEN, protocol=request.protocol)
        except NotFoundError:
            return Response(status_code=StatusCodes.NOT_FOUND, protocol=request.protocol)
        return Response(status_code=StatusCodes.OK, protocol=request.protocol,
                        content_length=resource.size, content_type=resource.content_type.value, body=b'')

    async def _execute_get_request(self, request: Request) -> Response:

        try:
            resource = self._build_resource(request)
        except ForbiddenError:
            return Response(status_code=StatusCodes.FORBIDDEN, protocol=request.protocol)
        except NotFoundError:
            if request.url[-1:] == '/':
                # return Response(status_code=StatusCodes.FORBIDDEN, protocol=request.protocol)
                pass
            else:
                return Response(status_code=StatusCodes.NOT_FOUND, protocol=request.protocol)

        if request.url[-1:] == '/':
            file_url = request.url[1:] + 'index.html'
        else:
            file_url = request.url[1:]

        filename = os.path.join(self._conf.document_root, file_url)

        try:
            content_type = ContentTypes[file_url.split('.')[-1]]
        except KeyError:
            content_type = ContentTypes.plain

        try:
            body = await self._reader.read(filename)
        except FileNotFoundError:
            if request.url[-1:] == '/':
                return Response(status_code=StatusCodes.FORBIDDEN, protocol=request.protocol)
            else:
                return Response(status_code=StatusCodes.NOT_FOUND, protocol=request.protocol)
        except NotADirectoryError:
            return Response(status_code=StatusCodes.NOT_FOUND, protocol=request.protocol)

        return Response(status_code=StatusCodes.OK,
                        protocol=request.protocol,
                        content_type=content_type.value,
                        content_length=len(body),
                        body=body)

    def _build_resource(self, request: Request) -> Resource:
        # get last el or empty string
        if request.url[-1:] == '/':
            file_url = request.url[1:] + 'index.html'
        else:
            file_url = request.url[1:]

        print(f"file_url: {file_url}")

        if len(file_url.split('../')) > 1:
            raise ForbiddenError

        filename = os.path.join(self._conf.document_root, file_url)

        try:
            size = os.path.getsize(filename)
        except OSError:
            raise NotFoundError

        try:
            content_type = ContentTypes[file_url.split('.')[-1]]
        except KeyError:
            content_type = ContentTypes.plain

        return Resource(filename=filename, file_url=file_url, content_type=content_type, size=size)