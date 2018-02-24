import logging

from asyncio import sleep


class Listener(object):

    def __init__(self) -> None:
        self._is_working: bool = False

    async def start(self) -> None:

        logging.info(f"[Listener] start")
        self._is_working = True

        while self._is_working:
            logging.info(f"[Listener] here the request will be processed")
            await sleep(5)

    def stop(self):
        logging.info(f"[Listener] stop")
        self._is_working = False


