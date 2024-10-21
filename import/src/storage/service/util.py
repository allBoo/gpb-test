import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from storage.data.models.maillog import Message, Log

logger = logging.getLogger(__name__)


class StorageService:
    def __init__(self, connection: AsyncSession) -> None:
        self.connection = connection
        self.models = [Message, Log]

    async def cleanup(self) -> None:
        await self.connection.begin()
        for model in self.models:
            logger.debug(f'Truncating {model.__tablename__}')
            await self.truncate(str(model.__tablename__))
        await self.connection.commit()

    async def truncate(self, table: str):
        await self.connection.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))
