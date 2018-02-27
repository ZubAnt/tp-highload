import socket
from asyncio import AbstractEventLoop, sleep
import logging

from configs.configure import Configure
from services.request_executor import RequestExecutor
from services.request_parser import RequestParser
from services.response_serializer import ResponseSerializer


class Worker(object):

    def __init__(self, loop: AbstractEventLoop, sock: socket, conf: Configure, pid: int = None) -> None:
        self._pid = pid
        self._loop = loop
        self._sock = sock
        self._conf = conf
        self._is_working: bool = False
        self._parser = RequestParser()
        self._executor = RequestExecutor(conf, loop)

    async def start(self, idx: int = None) -> None:

        """
        :param idx: index of worker
        :return: None
        """

        self._is_working = True

        while self._is_working:
            conn, addr = await self._loop.sock_accept(self._sock)

            data = b''
            while True:
                logging.debug(f"[Worker[{idx}]] [pid: {self._pid}] try read...")
                chunk = await self._loop.sock_recv(conn, self._conf.read_chunk_size)
                data += chunk
                logging.debug(f"[Worker[{idx}]] [pid: {self._pid}] chunk: {chunk}")

                if not chunk:
                    break

                lines = data.split(b'\n')

                if lines[-1] == b'':
                    break

                # await sleep(0.1)

            logging.debug(f"[Worker[{idx}]] [pid: {self._pid}] request package: {data}")

            request = self._parser.parse(data.decode())
            response = await self._executor.execute(request)
            data = ResponseSerializer.dump(response, request.method)
            await self._loop.sock_sendall(conn, data)
            logging.debug(f"[Worker[{idx}]] [pid: {self._pid}] response package: {data}")
            # await sleep(0.1)
            conn.close()

    def stop(self) -> None:
        self._is_working = False

