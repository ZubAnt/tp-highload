from asyncio import StreamReader, StreamWriter

from configs.connection import Connection
from configs.env_connection_factory import EnvConnectionFactory


class Handler(object):

    def __init__(self):
        self._connection = EnvConnectionFactory.create()

    @property
    def connection(self) -> Connection:
        return self._connection

    async def handle(self, reader: StreamReader, writer: StreamWriter) -> None:
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))

        print("Send: %r" % message)
        writer.write(data)
        await writer.drain()

        print("Close the client socket")
        writer.close()