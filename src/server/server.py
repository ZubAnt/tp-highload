from asyncio import AbstractEventLoop, start_server

from injector import singleton

from services.handler import Handler


@singleton
class Server(object):

    def __init__(self, loop: AbstractEventLoop):
        self._loop = loop
        self._handler = Handler()

    def start(self):
        self._loop.create_task(start_server(client_connected_cb=self._handler.handle,
                                            host=self._handler.connection.host,
                                            port=self._handler.connection.port,
                                            loop=self._loop))
