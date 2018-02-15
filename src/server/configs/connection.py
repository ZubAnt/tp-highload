class Connection(object):

    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port
