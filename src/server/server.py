from asyncio import AbstractEventLoop

from injector import singleton


@singleton
class Server(object):

    def __init__(self, loop: AbstractEventLoop):
        self._loop = loop

    def start(self):
        pass

    def stop(self):
        pass
