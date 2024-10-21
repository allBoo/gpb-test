from sqlalchemy.ext.asyncio import AsyncSession

from storage.data.models.maillog import Message, Log
from shared.data.db.repository import Repository


class MessageRepository(Repository[Message]):
    def __init__(self, conn: AsyncSession) -> None:
        super().__init__(conn, Message)


class LogRepository(Repository[Log]):
    def __init__(self, conn: AsyncSession) -> None:
        super().__init__(conn, Log)
