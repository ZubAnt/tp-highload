import logging
from asyncio import AbstractEventLoop

from configs.configure import Configure
from services.server import Server


class ServerManager(object):

    def __init__(self, loop: AbstractEventLoop, conf: Configure, pid: int = None):
        self._pid = pid
        self._loop = loop
        self._conf = conf
        self._server = Server(loop=loop, conf=conf, pid=None)

    def spawn(self) -> None:
        logging.info(f"[ServerManager] [pid: {self._pid}] listen on {self._conf.host}:{self._conf.port}; "
                     f"spawn {self._conf.workers} async workers...")
        for idx in range(self._conf.workers):
            self._loop.create_task(self._server.start_server_async())
