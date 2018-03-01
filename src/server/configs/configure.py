class Configure(object):

    def __init__(self, port: int,
                 document_root: str,
                 file_block_size: int,
                 cpu_count: int,
                 read_chunk_size: int,
                 write_chunk_size: int,
                 workers: int = None) -> None:
        self._host: str = '0.0.0.0'
        self._port = port
        self._document_root = document_root
        self._file_block_size = file_block_size
        self._cpu_count = cpu_count
        self._read_chunk_size = read_chunk_size
        self._worker = 1
        self._write_chunk_size = write_chunk_size
        self._workers = 1 if workers is None else workers

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def document_root(self) -> str:
        return self._document_root

    @property
    def file_block_size(self) -> int:
        return self._file_block_size

    @property
    def worker(self) -> int:
        return self._worker

    @property
    def cpu_count(self) -> int:
        return self._cpu_count

    @property
    def read_chunk_size(self) -> int:
        return self._read_chunk_size

    @property
    def write_chunk_size(self) -> int:
        return self._write_chunk_size

    @property
    def workers(self) -> int:
        return self._workers

