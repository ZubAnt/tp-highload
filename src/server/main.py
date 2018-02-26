import logging

from asyncio import get_event_loop

from configs.file_configure_factory import FileConfigureFactory
from configs.src_configure_factory import SrcConfigureFactory
from server import Server


def main():

    logging.basicConfig(level=logging.DEBUG)
    loop = get_event_loop()
    conf = FileConfigureFactory.create()
    server = Server(loop=loop, conf=conf)
    server.start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Receive STOP signal")
    except BaseException:
        logging.exception("Unhandled exception occurred - service stopped")


if __name__ == "__main__":
    main()
