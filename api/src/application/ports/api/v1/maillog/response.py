from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel

from search.data.dto.results import SearchItem


class Status(Enum):
    OK = "ok"
    ERROR = "error"


class SearchItemResponse(BaseModel):
    date: datetime
    log: str


class SearchResultResponse(BaseModel):
    items: list[SearchItemResponse]
    total: int


class ErrorResponse(BaseModel):
    message: str
