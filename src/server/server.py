import logging
from asyncio import AbstractEventLoop, start_server

from configs.configure import Configure
from services.handler import Handler


class Server(object):

    def __init__(self, loop: AbstractEventLoop, conf: Configure, pid: int = None) -> None:
        self._loop = loop
        self._pid = pid
        self._conf = conf
        self._handler = Handler(conf, loop, pid)

    def start(self):
        logging.info(f'Starting server on {self._conf.host}:{self._conf.port}')
        self._loop.create_task(start_server(client_connected_cb=self._handler.handle,
                                            host=self._conf.host,
                                            port=self._conf.port,
                                            loop=self._loop,
                                            reuse_port=True))

    async def start_server(self) -> None:
        await start_server(client_connected_cb=self._handler.handle,
                           host=self._conf.host,
                           port=self._conf.port,
                           loop=self._loop)
