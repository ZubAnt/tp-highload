from asyncio import AbstractEventLoop


import aiofiles

from configs.configure import Configure


class FileReader(object):

    def __init__(self, conf: Configure, loop: AbstractEventLoop):
        self._conf = conf
        self._loop = loop

    @classmethod
    async def read(cls, filename: str) -> bytes:
        async with aiofiles.open(filename, mode='rb') as f:
            return await f.read()

