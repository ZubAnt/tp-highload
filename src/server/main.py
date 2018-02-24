import logging

from asyncio import get_event_loop

from server import Server


def main():

    logging.basicConfig(level=logging.DEBUG)
    loop = get_event_loop()
    server = Server(loop=loop)
    server.start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Receive STOP signal")
    except BaseException:
        logging.exception("Unhandled exception occurred - service stopped")


if __name__ == "__main__":
    main()
