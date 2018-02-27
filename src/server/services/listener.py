import socket
from asyncio import AbstractEventLoop, sleep

from configs.configure import Configure
from services.request_executor import RequestExecutor
from services.request_parser import RequestParser
from services.response_serializer import ResponseSerializer


class Listener(object):

    def __init__(self, loop: AbstractEventLoop, conf: Configure, pid: int) -> None:
        self._pid = pid
        self._loop = loop
        self._conf = conf
        self._is_working: bool = False
        self._parser = RequestParser()
        self._executor = RequestExecutor(conf, loop)

    async def start(self, pid: int, sock: socket, loop: AbstractEventLoop) -> None:

        self._is_working = True

        while self._is_working:
            conn, addr = await loop.sock_accept(sock)

            data = b''
            while True:
                print(f"[Listener] [pid: {self._pid}] try read...")
                chunk = await loop.sock_recv(conn, self._conf.read_chunk_size)
                data += chunk
                print(f"[Listener] [pid: {self._pid}] chunk: {chunk}")

                if not chunk:
                    break

                lines = data.split(b'\n')

                if lines[-1] == b'':
                    break

            print(f"[Listener] [pid: {self._pid}] data: {data}")

            request = self._parser.parse(data.decode())
            print(f"[Listener] [pid: {self._pid}] completed parse request")
            response = await self._executor.execute(request)
            print(f"[Listener] [pid: {self._pid}] completed execute request")
            data = ResponseSerializer.dump(response, request.method)
            print(f"[Listener] [pid: {self._pid}] completed dump response")
            await loop.sock_sendall(conn, data)
            print(f"[Listener] [pid: {self._pid}] send data: {data}")
            conn.close()

    def stop(self) -> None:
        self._is_working = False

