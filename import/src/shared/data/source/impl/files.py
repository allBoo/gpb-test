import os
import logging
from typing import Any, TypeVar, Self, AsyncGenerator, Callable
from zipfile import ZipFile

from shared.data.source.exceptions import DataSourceError
from shared.data.source.interfaces import Reader

logger = logging.getLogger(__name__)

FilterCallback = Callable[[str], bool]


class FileReader(Reader[str]):
    """ TODO implement as bytes reader """

    def __init__(self, file: str) -> None:
        self.file = file
        self.filter: FilterCallback | None = None

    def filter(self, callback: FilterCallback) -> Self:
        self.filter = callback
        return self

    def _is_exists(self) -> bool:
        return os.path.exists(self.file) and os.path.isfile(self.file) and os.access(self.file, os.R_OK)

    async def read(self, fail_on_error=False, silent=False) -> AsyncGenerator[str, None]:
        if not self._is_exists():
            if fail_on_error:
                raise DataSourceError(f'File {self.file} does not exist')
            elif not silent:
                logger.error(f"File {self.file} not found")
            return

        with open(self.file, 'r') as file:
            for line in file:
                if self.filter is None or self.filter(line):
                    yield line.strip()

    async def read_one(self) -> str | None:
        if not self._is_exists():
            raise DataSourceError(f'File {self.file} does not exist')

        with open(self.file, 'r') as file:
            file_content = file.read()
            if self.filter is None or self.filter(file_content):
                return file_content

    async def close(self) -> None:
        pass


class ZipFileReader(FileReader):

    async def read(self, fail_on_error=False, silent=False) -> AsyncGenerator[str, None]:
        if not self._is_exists():
            raise DataSourceError(f'File {self.file} does not exist')

        with ZipFile(self.file, 'r') as zip_file:
            for name in zip_file.namelist():
                with zip_file.open(name) as myfile:
                    for line in myfile:
                        str_line = line.decode('utf-8').strip()
                        if self.filter is None or self.filter(str_line):
                            yield str_line

    async def read_one(self) -> str | None:
        if not self._is_exists():
            raise DataSourceError(f'File {self.file} does not exist')

        with ZipFile(self.file, 'r') as zip_file:
            for name in zip_file.namelist():
                with zip_file.open(name) as myfile:
                    file_content = myfile.read().decode('utf-8')
                    if self.filter is None or self.filter(file_content):
                        return file_content

        return None
