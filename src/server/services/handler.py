from asyncio import StreamReader, StreamWriter

from configs.configure import Configure


class Handler(object):

    def __init__(self, conf: Configure):
        self.conf = conf

    async def handle(self, reader: StreamReader, writer: StreamWriter) -> None:
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))

        send_msg = b"""HTTP/1.1 200 OK
        Server: nginx/1.2.1
        Date: Sat, 08 Mar 2014 22:53:46 GMT
        Content-Type: application/octet-stream
        Content-Length: 7
        Last-Modified: Sat, 08 Mar 2014 22:53:30 GMT
        Connection: keep-alive
        Accept-Ranges: bytes  
              

        Wisdom
        """

        print("Send: %r" % send_msg)
        writer.write(send_msg)
        await writer.drain()

        print("Close the client socket")
        writer.close()