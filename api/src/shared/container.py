from abc import ABC, abstractmethod

from shared.infrastructure.db import DataBase


class Container(ABC):

    @abstractmethod
    def get_database(self) -> DataBase:
        ...

