import os
from concurrent.futures import ThreadPoolExecutor

from asyncio import AbstractEventLoop
from typing import Optional

from configs.configure import Configure
from models.content_types import ContentTypes
from models.request import Request
from models.response import Response
from models.status_codes import StatusCodes
from services.file_reader import FileReader


class RequestExecutor(object):

    def __init__(self, conf: Configure, loop: AbstractEventLoop) -> None:
        self._conf = conf
        self._loop = loop
        self._reader = FileReader(conf, loop)

    async def execute(self, request: Request) -> Optional[Response]:
        if request.method not in ('GET', 'HEAD'):
            pass

        # get last el or empty string
        if request.url[-1:] == '/':
            file_url = request.url[1:] + 'index.html'
        else:
            file_url = request.url[1:]

        if len(file_url.split('../')) > 1:
            return Response(status_code=StatusCodes.FORBIDDEN, protocol=request.protocol)

        filename = os.path.join(self._conf.document_root, file_url)
        body = await self._reader.read(filename)

        try:
            content_type = ContentTypes[file_url.split('.')[-1]].value
        except KeyError:
            content_type = ContentTypes.text_plain

        content_length = len(body)

        return Response(status_code=StatusCodes.OK,
                        protocol=request.protocol,
                        content_type=content_type,
                        content_length=content_length,
                        body=body)


