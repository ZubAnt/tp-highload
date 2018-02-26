from asyncio import AbstractEventLoop, sleep
from concurrent.futures import ThreadPoolExecutor

from configs.configure import Configure


class FileReader(object):

    def __init__(self, conf: Configure, loop: AbstractEventLoop):
        self._conf = conf
        self._loop = loop
        self._executor = ThreadPoolExecutor(max_workers=conf.cpu_count)

    async def read(self, filename: str) -> bytes:
        data: bytes = b""
        file = open(filename, 'rb')
        while True:
            chunk = await self._loop.run_in_executor(self._executor, file.read, self._conf.read_chunk_size)
            await sleep(0)
            if chunk == b'':
                break
            data += chunk
        return data
