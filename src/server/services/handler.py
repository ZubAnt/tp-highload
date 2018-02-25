from asyncio import StreamReader, StreamWriter, sleep, IncompleteReadError, AbstractEventLoop

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
        i = 0
        while True:
            print(f"try read {i} block...")

            block = await reader.read(self._conf.read_chunk_size)
            # print(f"block[{i}] = {block}")
            # print(f"total: {self._conf.read_chunk_size} bytes; actual: {len(block)} bytes")
            # print(f"reader.at_eof() = {reader.at_eof()}")
            # print(f"reader buffer: {reader._buffer}")
            # print(f"reader eof: {reader._eof}")
            # print()

            blocks.append(block)
            i += 1

            if not block or reader.at_eof():
                break

            if reader._buffer == b'':
                break

        data: str = b''.join(blocks).decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (data, addr))

        request = self._parser.parse(data)
        response = await self._executor.execute(request)
        data = ResponseSerializer.dump(response)


        send_msg = b"""HTTP/1.1 200 OK
        Server: nginx/1.2.1
        Date: Sat, 08 Mar 2014 22:53:46 GMT
        Content-Type: application/octet-stream
        Content-Length: 7
        Last-Modified: Sat, 08 Mar 2014 22:53:30 GMT
        Connection: keep-alive
        Accept-Ranges: bytes  
              

        Wisdom
        """

        print("Send: %r" % send_msg)
        writer.write(data)
        await writer.drain()

        print("Close the client socket")
        writer.close()
