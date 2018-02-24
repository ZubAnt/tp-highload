import logging
from asyncio import AbstractEventLoop, start_server

from configs.configure import Configure
from services.handler import Handler


class Server(object):

    def __init__(self, loop: AbstractEventLoop, conf: Configure) -> None:
        self._loop = loop
        self._conf = conf
        self._handler = Handler(conf)

    def start(self):
        logging.info('add start_server coro')
        self._loop.create_task(start_server(client_connected_cb=self._handler.handle,
                                            host=self._conf.host,
                                            port=self._conf.port,
                                            loop=self._loop))
