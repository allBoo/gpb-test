import enum
from datetime import datetime

from pydantic import BaseModel


class ResultType(enum.StrEnum):
    LOG = 'LOG'
    MESSAGE = 'MESSAGE'


class SearchItem(BaseModel):
    int_id: str
    created: datetime
    str: str
    type: ResultType


class SearchResults(BaseModel):
    items: list[SearchItem]
    total: int
