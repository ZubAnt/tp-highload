import asyncio
import logging
from asyncio import AbstractEventLoop, sleep
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from fcntl import fcntl, F_SETFL, F_GETFL

import os

from configs.configure import Configure


class FileReader(object):

    def __init__(self, conf: Configure, loop: AbstractEventLoop):
        self._conf = conf
        self._loop = loop
        self._executor = ThreadPoolExecutor()

    async def read(self, filename: str) -> bytes:
        data: bytes = b""
        file = open(filename, 'rb')
        fd = file.fileno()
        flag = fcntl(fd, F_GETFL)
        fcntl(fd, F_SETFL, flag | os.O_NONBLOCK)
        flag = fcntl(fd, F_GETFL)
        if flag & os.O_NONBLOCK:
            logging.info(f"[FileReader] flag & os.O_NONBLOCK")
        else:
            logging.info(f"[FileReader] not")

        logging.info(f"[FileReader] try read {filename}")
        logging.info(f"[FileReader] loop status: {self._loop.is_running()}")
        while True:
            logging.debug(f"[FileReader] try read...")
            #
            chunk = await self._loop.run_in_executor(self._executor, file.read, self._conf.read_chunk_size)
            # chunk = await self._read(file, 32)
            # chunk = self._executor.submit(self._read_sync_chunk, file, 64)
            logging.debug(f"[FileReader] chunk: {chunk}")
            await sleep(0)
            if chunk == b'':
                break
            data += chunk
        file.close()
        return data

    @asyncio.coroutine
    def _read(self, file, chunk_size):
        yield from file.read(chunk_size)

    @classmethod
    def _read_sync_chunk(cls, file, chunk_size):
        return file.read(chunk_size)


