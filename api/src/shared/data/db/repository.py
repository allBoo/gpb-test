from typing import Generic, TypeVar, Type, Union, Iterable, Any

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from shared.data.db.model import BaseModel
from pydantic import BaseModel as Dto

T = TypeVar('T', bound=BaseModel)
DT = TypeVar('DT', bound=Dto, covariant=True)
PK = Union[int, str]


class Repository(Generic[T]):
    def __init__(self, conn: AsyncSession, cls: Type[T]) -> None:
        self._conn = conn
        self._cls = cls

    def get_queryset(self) -> sa.sql.Select:
        return sa.select(self._cls)

    async def get_by_id(self, entity_id: PK) -> Union[T, None]:
        return await self._conn.scalar(
            sa.select(self._cls).where(self._cls.id == entity_id)
        )

    async def get_by_ids(self, entity_ids: list[PK]) -> dict[PK, T]:
        res = await self._conn.scalars(
            sa.select(self._cls).where(self._cls.id.in_(entity_ids))
        )
        return {item.id: item for item in res}

    async def add(self, entity: Union) -> None:
        return self._conn.add(entity)

    async def add_dto(self, entity: DT) -> None:
        await self.add(self._cls.from_dto(entity))

    async def bulk_insert(self, entities: Iterable[T]) -> None:
        if not entities:
            return
        return self._conn.add_all(entities)

    async def bulk_insert_dtos(self, entities: Iterable[DT]) -> None:
        if not entities:
            return
        await self.bulk_insert([self._cls.from_dto(e) for e in entities])

    async def update(self, entity_id: PK, values: dict) -> int:
        res = await self._conn.execute(
            self._cls.__table__.update().where(self._cls.id == entity_id).values(**values)
        )
        return res.rowcount()

    async def delete_by(self, where: dict[str, Any]) -> int:
        res = await self._conn.execute(
            self._cls.__table__.delete().filter_by(**where)
        )
        return res.rowcount
