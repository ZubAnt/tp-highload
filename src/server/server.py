from asyncio import AbstractEventLoop

from injector import singleton

from services.listener import Listener


@singleton
class Server(object):

    def __init__(self, loop: AbstractEventLoop):
        self._loop = loop
        self._listener = Listener()

    def start(self):
        self._loop.create_task(self._listener.start())

    def stop(self):
        self._listener.stop()
