from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from pydantic import BaseModel

from shared.data.source.interfaces import Reader, Writer


T = TypeVar('T', bound=BaseModel)


class ReadDataSource(Generic[T], ABC):
    @abstractmethod
    def get_reader(self) -> Reader[T]:
        raise NotImplementedError


class WriteDataSource(Generic[T], ABC):
    @abstractmethod
    def get_writer(self) -> Writer[T]:
        raise NotImplementedError


class DataSource(Generic[T], ReadDataSource[T], WriteDataSource[T], ABC):
    pass
