class ExternalConfigure(object):
    
    def __init__(self, listen: int, cpu_limit: int, thread_limit: int, document_root: str):
        self._listen = listen
        self._cpu_limit = cpu_limit
        self._thread_limit = thread_limit
        self._document_root = document_root

    @property
    def listen(self) -> int:
        return self._listen

    @property
    def cpu_limit(self) -> int:
        return self._cpu_limit

    @property
    def thread_limit(self) -> int:
        return self._thread_limit

    @property
    def document_root(self) -> str:
        return self._document_root
