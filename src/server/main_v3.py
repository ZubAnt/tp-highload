import logging

from asyncio import get_event_loop

import os
from socket import *

import fcntl

from configs.file_configure_factory import FileConfigureFactory
from configs.src_configure_factory import SrcConfigureFactory
from server import Server
from services.listener import Listener

forks = []


if __name__ == "__main__":

    conf = SrcConfigureFactory.create()

    # sock = socket(AF_INET, SOCK_STREAM)
    # sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # sock.bind((conf.host, conf.port))
    # fcntl.fcntl(sock, fcntl.F_SETFL, os.O_NONBLOCK)
    #
    # # number of connections in the queue
    # sock.listen(10)

    loop = get_event_loop()

    for x in range(0, conf.cpu_count):
        pid = os.fork()
        forks.append(pid)
        if pid == 0:
            loop = get_event_loop()
            server = Server(loop=loop, conf=conf, pid=os.getpid())
            server.start()
            print('PID:', os.getpid())

    loop.run_forever()

    for pid in forks:
        os.waitpid(pid, 0)
