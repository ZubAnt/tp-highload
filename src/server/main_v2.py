import logging

from asyncio import get_event_loop

import os
from socket import *

import fcntl

from configs.file_configure_factory import FileConfigureFactory
from configs.src_configure_factory import SrcConfigureFactory
from services.worker_manager import WorkerManager

forks = []


if __name__ == "__main__":

    conf = FileConfigureFactory.create()

    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)

    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((conf.host, conf.port))
    # fcntl.fcntl(sock, fcntl.F_SETFL, os.O_NONBLOCK)

    # number of connections in the queue
    sock.listen(32)

    for x in range(0, conf.cpu_count):
        pid = os.fork()
        forks.append(pid)
        if pid == 0:
            loop = get_event_loop()
            manager = WorkerManager(loop=loop, sock=sock, conf=conf, workers=1, pid=os.getpid())
            manager.spawn()
            loop.close()

    for pid in forks:
        os.waitpid(pid, 0)


