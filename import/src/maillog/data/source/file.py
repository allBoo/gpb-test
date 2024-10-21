from maillog.data.models.maillog import MailLog
from shared.data.source import ReadDataSource, Reader
from shared.data.source.impl.files import FileReader
from shared.data.source.transform.stream import StreamTransformer

from maillog.service.parser import MailLogParser


class FileDataSource(ReadDataSource[MailLog]):
    def __init__(self, file_reader: FileReader):
        self.reader = file_reader

    def get_reader(self) -> Reader[MailLog]:
        return StreamTransformer[MailLog](self.reader, MailLogParser.from_string)
