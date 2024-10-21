from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from maillog.data.models.maillog import MailLog
from shared.container import Container
from shared.data.source import WriteDataSource
from storage.data.source.maillog import MaillogDatabaseDataSource
from storage.service.util import StorageService


class StorageFactory:

    @staticmethod
    def get_data_sink(connection: AsyncSession) -> WriteDataSource[MailLog]:
        return MaillogDatabaseDataSource(connection)

    @staticmethod
    def get_storage_service(connection: AsyncSession) -> StorageService:
        return StorageService(connection)
