import asyncio
import logging

from asyncio import get_event_loop

import os
import uvloop

from configs.file_configure_factory import FileConfigureFactory
from configs.src_configure_factory import SrcConfigureFactory
from services.server_manager import ServerManager

forks = []


if __name__ == "__main__":

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    conf = FileConfigureFactory.create()

    logging.basicConfig(level=logging.INFO)

    for _ in range(0, conf.cpu_count):
        pid = os.fork()
        forks.append(pid)

        if pid == 0:
            loop = get_event_loop()
            manager = ServerManager(loop, conf, os.getpid())
            manager.spawn()
            loop.run_forever()

    for pid in forks:
        os.waitpid(pid, 0)


