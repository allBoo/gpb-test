import logging
from typing import Any, TypeVar, Self, AsyncGenerator, Callable

from pydantic import BaseModel as Dto
from sqlalchemy import ColumnExpressionArgument

from shared.data.db.model import BaseModel
from shared.data.db.repository import Repository
from shared.data.source import Writer
from shared.data.source.interfaces import Reader

TD = TypeVar('TD', bound=Dto, covariant=True)
TB = TypeVar('TB', bound=BaseModel, covariant=True)

logger = logging.getLogger(__name__)


class DatabaseReader(Reader[TD]):
    def __init__(self, repository: Repository, model: TD):
        self.repository = repository
        self.model = model
        self.query = self.repository.get_queryset()

    def filter(self, criteria: ColumnExpressionArgument) -> Self:
        self.query = self.query.where(criteria)
        return self

    async def read(self, fail_on_error=False, silent=False) -> AsyncGenerator[TD, None]:
        async with self.repository._conn.begin():
            for item in await self.repository._conn.scalars(self.query):
                yield self.model.model_validate(item, from_attributes=True)

    async def read_one(self) -> TD | None:
        async with self.repository._conn.begin():
            result = await self.repository._conn.execute(self.query)
            item = result.first()
            if item:
                return self.model.model_validate(item.first(), from_attributes=True)
            return None

    async def close(self) -> None:
        pass


class DatabaseWriter(Writer[TB]):
    def __init__(self, repository: Repository, model: TB):
        self.repository = repository
        self.model = model

    async def __aenter__(self) -> Self:
        if self.repository._conn.in_transaction():
            self.transaction = await self.repository._conn.begin_nested()
        else:
            self.transaction = await self.repository._conn.begin()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.repository._conn.in_transaction():
            if exc_type is None:
                await self.transaction.commit()
            else:
                await self.transaction.rollback()

    async def write(self, data: TB, on_failure: Callable[[TB], None] | None = None) -> TB:
        try:
            await self.repository.add(data)
        except Exception as e:
            if on_failure:
                on_failure(data)
            logger.exception(e)
        return data

    async def write_to(self, target: Repository, data: TD, on_failure: Callable[[TB], None] | None = None) -> TB:
        try:
            await target.add(data)
        except Exception as e:
            if on_failure:
                on_failure(data)
            logger.exception(e)
        return data

    async def close(self) -> None:
        if self.repository._conn.is_active:
            await self.repository._conn.close()


class DatabaseDtoWriter(DatabaseWriter[TD]):
    async def write(self, data: TD, on_failure: Callable[[TD], None] | None = None) -> TD:
        try:
            await self.repository.add_dto(data)
        except Exception as e:
            if on_failure:
                on_failure(data)
            logger.exception(e)
        return data

    async def write_to(self, target: Repository, data: TD, on_failure: Callable[[TD], None] | None = None) -> TD:
        try:
            await target.add_dto(data)
        except Exception as e:
            if on_failure:
                on_failure(data)
            logger.exception(e)
        return data
