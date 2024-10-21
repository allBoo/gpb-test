from functools import partial

from maillog.data.models.maillog import MailLog
from maillog.data.source.file import FileDataSource
from maillog.data.types import FileType
from shared.data.source import ReadDataSource

from shared.data.source.impl.files import FileReader, ZipFileReader


class SourceFactory:

    FILE_TYPE_SOURCE_MAP = {
        FileType.Plain: FileReader,
        FileType.Zip: ZipFileReader,
    }

    @classmethod
    def get_data_source(cls, file: str, data_type: FileType) -> ReadDataSource[MailLog]:
        file_reader_cls = cls.FILE_TYPE_SOURCE_MAP.get(data_type)
        if not file_reader_cls:
            raise ValueError(f"FileReader for data type {data_type} not found")

        file_reader = file_reader_cls(file)

        return FileDataSource(file_reader)
