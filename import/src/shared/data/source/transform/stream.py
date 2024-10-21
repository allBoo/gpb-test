import logging
from typing import Any, TypeVar, Self, AsyncGenerator, Callable

from pydantic import BaseModel

from shared.data.source.exceptions import InvalidData
from shared.data.source.interfaces import Reader

T = TypeVar('T', bound=BaseModel, covariant=True)

SourceStream = Reader[Any]
StreamParser = Callable[[Any], T | None]
FilterCallback = Callable[[T], bool]

logger = logging.getLogger(__name__)


class StreamTransformer(Reader[T]):
    def __init__(self, stream: SourceStream, transformer: StreamParser):
        self.stream = stream
        self.parser = transformer
        self.filter: FilterCallback | None = None

    def filter(self, callback: FilterCallback) -> Self:
        self.filter = callback
        return self

    async def read(self, fail_on_error=False, silent=False) -> AsyncGenerator[T, None]:
        async for item in self.stream.read(fail_on_error, silent):
            try:
                model = self.parser(item)
            except Exception as e:
                if not silent:
                    logger.exception(f"Error while parse item: {item}")
                if fail_on_error:
                    raise InvalidData(item)
                continue

            if not model:
                if not silent:
                    logger.error(f"Failed to parse item: {item}")
                if fail_on_error:
                    raise InvalidData(item)
                continue

            if self.filter is None or self.filter(model):
                yield model

    async def read_one(self) -> T | None:
        item = await self.stream.read_one()
        if item:
            model = self.parser(item)
            if self.filter is None or self.filter(model):
                return model
        return None

    async def close(self) -> None:
        await self.stream.close()
