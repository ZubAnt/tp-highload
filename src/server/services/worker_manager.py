import logging
import socket
from asyncio import AbstractEventLoop, gather

from configs.configure import Configure
from services.worker import Worker


class WorkerManager(object):

    def __init__(self, loop: AbstractEventLoop, sock: socket,
                 conf: Configure, workers: int = None, pid: int = None) -> None:
        self._pid = pid
        self._sock = sock
        self._conf = conf
        self._loop = loop
        self._workers = 1 if workers is None else workers
        self._worker = Worker(loop=self._loop, sock=self._sock, conf=self._conf, pid=self._pid)

    def spawn(self) -> None:
        """
        spawn workers in loop
        :return: None
        """
        logging.info(f"[WorkerManager] [pid: {self._pid}] listen on {self._conf.host}:{self._conf.port}; "
                     f"spawning {self._workers} workers...")

        # for idx in range(self._workers):
        #     self._loop.run_until_complete(self._worker.start(idx))
        #     self._loop.close()


        #############################################################################


        collection = list()
        for idx in range(self._workers):
            collection += [self._worker.start(idx)]
            logging.debug(f"[WorkerManager] spawn {idx} worker")
            self._loop.create_task(self._worker.start(idx))
        logging.debug(f"[WorkerManager] collection of workers: {collection}")
        feature = gather(*tuple(collection))
        self._loop.run_until_complete(feature)
        self._loop.close()

    def stop(self):
        self._worker.stop()
