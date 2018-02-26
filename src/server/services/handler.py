from asyncio import StreamReader, StreamWriter, sleep, AbstractEventLoop

from configs.configure import Configure
from services.request_executor import RequestExecutor
from services.request_parser import RequestParser
from services.response_serializer import ResponseSerializer


class Handler(object):
    def __init__(self, conf: Configure, loop: AbstractEventLoop):
        self._conf = conf
        self._parser = RequestParser()
        self._executor = RequestExecutor(conf, loop)

    async def handle(self, reader: StreamReader, writer: StreamWriter) -> None:

        blocks = []
        while True:
            block = await reader.read(self._conf.read_chunk_size)
            blocks.append(block)

            if not block or reader.at_eof() or reader._buffer == b'':
                break

            await sleep(0)

        data: str = b''.join(blocks).decode()
        request = self._parser.parse(data)
        response = await self._executor.execute(request)
        data = ResponseSerializer.dump(response)

        writer.write(data)
        await writer.drain()

        writer.close()
