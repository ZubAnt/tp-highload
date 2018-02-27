from asyncio import AbstractEventLoop

from configs.configure import Configure
from server import Server


class ServerManager(object):

    def __init__(self, loop: AbstractEventLoop, conf: Configure, workers: int = None):
        self._loop = loop
        self._conf = conf
        self._workers = 1 if workers is None else workers
        self._server = Server(loop=loop, conf=conf)

    def spawn(self) -> None:
        for idx in range(self._workers):
            self._loop.create_task(self._server.start_server(idx))
