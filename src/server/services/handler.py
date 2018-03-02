import logging
from asyncio import StreamReader, StreamWriter, sleep, AbstractEventLoop

from configs.configure import Configure
from services.request_executor import RequestExecutor
from services.request_parser import RequestParser
from services.response_serializer import ResponseSerializer


class Handler(object):

    def __init__(self, conf: Configure, loop: AbstractEventLoop, pid: int = None, idx: int = None):
        self._idx = idx
        self._pid = pid
        self._conf = conf
        self._parser = RequestParser()
        self._executor = RequestExecutor(conf, loop)

    async def handle(self, reader: StreamReader, writer: StreamWriter) -> None:

        data = b''
        while True:
            logging.debug(f"[Handler] try read...")
            chunk = await reader.read(self._conf.read_chunk_size)
            logging.debug(f"[Handler] chunk: {chunk}")
            data += chunk

            if not chunk or reader.at_eof():
                break

            lines = data.split(b'\n')

            if lines[-1] == b'':
                break

        logging.debug(f"[Handler] data: {data}")

        request = self._parser.parse(data.decode())
        response = await self._executor.execute(request)
        data = ResponseSerializer.dump(response)
        writer.write(data)
        await writer.drain()
        writer.close()
