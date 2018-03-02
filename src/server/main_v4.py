import asyncio
import logging

from asyncio import get_event_loop

import os
from socket import *

import fcntl

import uvloop

from configs.file_configure_factory import FileConfigureFactory
from configs.src_configure_factory import SrcConfigureFactory
from services.server_manager import ServerManager
from services.worker_manager import WorkerManager

forks = []


if __name__ == "__main__":

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # conf = FileConfigureFactory.create()
    conf = SrcConfigureFactory.create()

    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)

    for x in range(0, conf.cpu_count):
        pid = os.fork()
        forks.append(pid)
        if pid == 0:

            loop = get_event_loop()
            manager = ServerManager(loop, conf, workers=conf.workers)
            manager.spawn()
            loop.run_forever()

    for pid in forks:
        os.waitpid(pid, 0)


