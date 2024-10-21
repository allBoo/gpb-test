from typing import Any

from shared.container import Container
from shared.infrastructure.db import DataBase
from config import Config


class ApplicationContainer(Container):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.services: dict[str, Any] = {}

    def get_database(self) -> DataBase:
        if 'database' not in self.services:
            self.services['database'] = DataBase(str(self.config.DATABASE_DSN))

        return self.services['database']
