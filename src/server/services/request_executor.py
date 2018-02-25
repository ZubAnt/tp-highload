import os
from concurrent.futures import ThreadPoolExecutor

from asyncio import AbstractEventLoop
from typing import Optional

from configs.configure import Configure
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
        data = await self._reader.read(filename)
        print(data)
        return None



