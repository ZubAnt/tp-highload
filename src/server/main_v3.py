import logging

from asyncio import get_event_loop

from configs.file_configure_factory import FileConfigureFactory
from configs.src_configure_factory import SrcConfigureFactory

from services.server_manager import ServerManager


def main():
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)

    conf = SrcConfigureFactory.create()

    loop = get_event_loop()
    manager = ServerManager(loop, conf, workers=100)
    manager.spawn()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Receive STOP signal")
    except BaseException:
        logging.exception("Unhandled exception occurred - service stopped")


if __name__ == "__main__":
    main()
