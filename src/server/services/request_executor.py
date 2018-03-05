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
        try:
            content_length = self._build_content_length(resource=resource)
        except NotFoundError:
            return Response(status_code=StatusCodes.NOT_FOUND, protocol=request.protocol)

        return Response(status_code=StatusCodes.OK, protocol=request.protocol,
                        content_length=content_length, content_type=resource.content_type.value, body=b'')

    async def _execute_get_request(self, request: Request) -> Response:

        try:
            resource = self._build_resource(request)
        except ForbiddenError:
            return Response(status_code=StatusCodes.FORBIDDEN, protocol=request.protocol)

        if not os.path.exists(resource.filename):
            if request.path[-1:] == '/':
                return Response(status_code=StatusCodes.FORBIDDEN, protocol=request.protocol)
            else:
                return Response(status_code=StatusCodes.NOT_FOUND, protocol=request.protocol)

        try:
            body = await self._reader.read(resource.filename)
        except FileNotFoundError:
            if request.path[-1:] == '/':
                return Response(status_code=StatusCodes.FORBIDDEN, protocol=request.protocol)
            else:
                return Response(status_code=StatusCodes.NOT_FOUND, protocol=request.protocol)
        except NotADirectoryError:
            return Response(status_code=StatusCodes.NOT_FOUND, protocol=request.protocol)

        return Response(status_code=StatusCodes.OK,
                        protocol=request.protocol,
                        content_type=resource.content_type.value,
                        content_length=len(body),
                        body=body)

    def _build_resource(self, request: Request) -> Resource:

        file_path = self._build_file_path(request.path)

        if len(file_path.split('../')) > 1:
            raise ForbiddenError

        filename = os.path.join(self._conf.document_root, file_path)
        content_type = self._build_content_type(file_path=file_path)

        return Resource(filename=filename, file_path=file_path, content_type=content_type)

    @classmethod
    def _build_content_length(cls, resource: Resource) -> int:
        try:
            return os.path.getsize(resource.filename)
        except OSError:
            raise NotFoundError

    @classmethod
    def _build_file_path(cls, path: str) -> str:
        # get last el or empty string
        if path[-1:] == '/':
            return path[1:] + 'index.html'
        else:
            return path[1:]

    @classmethod
    def _build_content_type(cls, file_path) -> ContentTypes:
        try:
            return ContentTypes[file_path.split('.')[-1]]
        except KeyError:
            return ContentTypes.plain

