from models.content_types import ContentTypes


class Resource(object):

    def __init__(self, filename: str = None, file_path: str = None, content_type: ContentTypes = None) -> None:
        self._filename = filename
        self._file_path = file_path
        self._content_type = content_type

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def content_type(self) -> ContentTypes:
        return self._content_type
