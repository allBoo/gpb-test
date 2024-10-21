import logging
from typing import Any, TypeVar, Self, Hashable, Callable

from pydantic import BaseModel

from shared.data.source.exceptions import InvalidData
from shared.data.source.interfaces import Writer

ATOM = TypeVar('ATOM', bound=Hashable)
T = TypeVar('T', bound=BaseModel, covariant=True)

StreamRouter = Callable[[Any], ATOM]
SinkMap = dict[ATOM, Writer[Any]]

logger = logging.getLogger(__name__)


class MultiSink(Writer[T]):
    def __init__(self, router: StreamRouter, sinks: SinkMap) -> None:
        self.router = router
        self.sinks = sinks

    async def __aenter__(self) -> Self:
        self._sink_contexts = {key: await sink.__aenter__() for key, sink in self.sinks.items()}
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        for sink in self._sink_contexts.values():
            await sink.__aexit__(exc_type, exc_val, exc_tb)

    async def write(self, data: T, on_failure: Callable[[Any], None] | None = None) -> T:
        route = self.router(data)
        sink = self.sinks.get(route)
        if sink:
            return await sink.write(data, on_failure)
        else:
            logger.error(f"No sink found for route: {route}")
            if on_failure:
                on_failure(data)
        return data

    async def write_to(self, target: Any, data: T, on_failure: Callable[[Any], None] | None = None) -> T:
        atom = self.router(data)
        sink = self.sinks.get(atom)
        if sink:
            return await sink.write_to(target, data, on_failure)
        else:
            logger.error(f"No sink found for atom: {atom}")
            if on_failure:
                on_failure(data)
        return data

    async def close(self) -> None:
        for sink in self.sinks.values():
            await sink.close()
