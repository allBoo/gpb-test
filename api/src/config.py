import os
from configparser import ConfigParser
from typing import Any, TypeAlias, Self

from pydantic import Field, KafkaDsn, PostgresDsn, ClickHouseDsn, BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):

    @classmethod
    def from_config_file(cls, path: str) -> Self:
        config = ConfigParser()
        config.read(path)

        if config.has_section('app'):
            return cls(**config['app'])
        else:
            raise ValueError('Section "app" not found in config')


class Config(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)

    DEBUG: bool = Field(default=False)
    ALLOWED_HOSTS: list[str] = Field(default_factory=lambda: os.getenv('ALLOWED_HOSTS', '*').split(','))

    DATABASE_DSN: PostgresDsn = Field(default='postgresql+asyncpg://gpb:gpb@db:5432/gpb')

    app_config: AppConfig | None = None

    def update(self, key: str, value: Any) -> None:
        typ_ = type(self.__getattribute__(key))
        self.__setattr__(key, typ_(value))


settings = Config()
