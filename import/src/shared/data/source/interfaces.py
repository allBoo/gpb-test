from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Any, TypeVar, Self, Callable, AsyncGenerator

TR = TypeVar('TR', covariant=True)
TW = TypeVar('TW')


class Reader(Generic[TR], ABC):
    @abstractmethod
    def filter(self, criteria: Any) -> Self:
        ...

    @abstractmethod
    async def read_one(self) -> TR | None:
        ...

    @abstractmethod
    async def read(self, fail_on_error=False, silent=False) -> AsyncGenerator[TR, None]:
        yield NotImplementedError  # type: ignore

    @abstractmethod
    async def close(self) -> None:
        ...


class Writer(Generic[TW]):
    async def __aenter__(self) -> Self:
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        raise NotImplementedError

    @abstractmethod
    async def write(self, data: TW, on_failure: Callable[[TW], None] | None = None) -> TW:
        ...

    @abstractmethod
    async def write_to(self, target: Any, data: TW, on_failure: Callable[[TW], None] | None = None) -> TW:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...
