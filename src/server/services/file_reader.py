from asyncio import AbstractEventLoop, sleep
from concurrent.futures import ThreadPoolExecutor

from configs.configure import Configure


class FileReader(object):

    def __init__(self, conf: Configure, loop: AbstractEventLoop):
        self._conf = conf
        self._loop = loop
        self._executor = ThreadPoolExecutor(max_workers=conf.cpu_count)

    async def read(self, filename: str) -> str:
        data: str = ""
        file = open(filename)
        while True:
            chunk = await self._loop.run_in_executor(self._executor, file.read, self._conf.read_chunk_size)
            await sleep(0)
            # print(f"[FileReader.read] chunk: {chunk}")
            # print()
            if chunk == '':
                break
            data += chunk
        print(f"[FileReader.read] type of data: {type(data)}")
        return data
