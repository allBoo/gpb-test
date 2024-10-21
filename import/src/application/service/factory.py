from sqlalchemy.ext.asyncio import AsyncSession

from application.service.importer import Importer

from maillog.data.types import FileType
from maillog.service.factory import SourceFactory
from storage.service.factory import StorageFactory
from storage.service.util import StorageService


class ServiceFactory:

    @staticmethod
    def get_import_service(connection: AsyncSession, file: str, zipped: bool = False, gzipped: bool = False) -> Importer:
        file_type = FileType.Zip if zipped else FileType.Gzip if gzipped else FileType.Plain

        data_source = SourceFactory.get_data_source(file, file_type)
        reader = data_source.get_reader()

        data_sink = StorageFactory.get_data_sink(connection)
        writer = data_sink.get_writer()

        return Importer(reader, writer)

    @staticmethod
    def get_storage_service(connection: AsyncSession) -> StorageService:
        return StorageService(connection)
