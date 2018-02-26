from models.content_types import ContentTypes


class Resource(object):

    def __init__(self, filename: str = None, file_url: str = None, size: int = None,
                 content_type: ContentTypes = None) -> None:
        self._filename = filename
        self._file_url = file_url
        self._size = size
        self._content_type = content_type

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def file_url(self) -> str:
        return self._file_url

    @property
    def size(self) -> int:
        return self._size

    @property
    def content_type(self) -> ContentTypes:
        return self._content_type
