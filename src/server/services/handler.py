from asyncio import StreamReader, StreamWriter, sleep, AbstractEventLoop

from configs.configure import Configure
from services.request_executor import RequestExecutor
from services.request_parser import RequestParser
from services.response_serializer import ResponseSerializer


class Handler(object):

    def __init__(self, conf: Configure, loop: AbstractEventLoop, pid: int = None):
        self._pid = pid
        self._conf = conf
        self._parser = RequestParser()
        self._executor = RequestExecutor(conf, loop)

    async def handle(self, reader: StreamReader, writer: StreamWriter) -> None:

        data = b''
        while True:
            print(f"[Listener] [pid: {self._pid}] try read...")
            chunk = await reader.read(self._conf.read_chunk_size)
            print(f"[Listener] [pid: {self._pid}] chunk: {chunk}")
            data += chunk

            if not chunk or reader.at_eof():
                break

            lines = data.split(b'\n')

            if lines[-1] == b'':
                break

        print(f"[Listener] [pid: {self._pid}] data: {data}")

        request = self._parser.parse(data.decode())
        print(f"[Listener] [pid: {self._pid}] completed parse request")
        response = await self._executor.execute(request)
        print(f"[Listener] [pid: {self._pid}] completed execute request")

        data = ResponseSerializer.dump(response)
        print(f"[Listener] [pid: {self._pid}] completed dump response")

        writer.write(data)
        await writer.drain()
        print(f"[Listener] [pid: {self._pid}] send data: {data}")

        writer.close()
