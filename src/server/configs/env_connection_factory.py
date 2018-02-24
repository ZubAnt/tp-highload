import os

from configs.connection import Connection


class EnvConnectionFactory(object):

    @staticmethod
    def create() -> Connection:
        host = os.environ.get('ACCEPT_HOST', None)
        port = os.environ.get('ACCEPT_PORT', None)

        if not host:
            host = 'localhost'

        if not port:
            port = 8080

        return Connection(host=host, port=port)
