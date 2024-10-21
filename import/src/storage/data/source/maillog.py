import enum

from sqlalchemy.ext.asyncio import AsyncSession

from maillog.data.models.maillog import MailLog, MessageType
from shared.data.source import WriteDataSource, Writer
from shared.data.source.impl.database import DatabaseDtoWriter
from shared.data.source.sink.multisink import MultiSink
from storage.data.models.maillog import Message, Log
from storage.data.repository.maillog import MessageRepository, LogRepository


class ModelType(str, enum.Enum):
    message = "message"
    log = "log"


class MaillogDatabaseDataSource(WriteDataSource[MailLog]):

    def __init__(self, connection: AsyncSession) -> None:
        messages_repo = MessageRepository(connection)
        messages_writer = DatabaseDtoWriter[Message](messages_repo, Message)

        logs_repo = LogRepository(connection)
        logs_writer = DatabaseDtoWriter[Log](logs_repo, Log)

        self.sink_map = {
            ModelType.message: messages_writer,
            ModelType.log: logs_writer
        }

    def get_writer(self) -> Writer[MailLog]:
        return MultiSink[MailLog](self.route, self.sink_map)

    @staticmethod
    def route(data: MailLog) -> ModelType:
        return ModelType.message if data.type == MessageType.incoming else ModelType.log
