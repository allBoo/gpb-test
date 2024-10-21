import enum
from datetime import datetime

from pydantic import BaseModel, Field


class MessageType(str, enum.Enum):
    incoming = '<='
    outcoming = '=>'
    additional = '->'
    error = '**'
    delay = '=='
    other = ''


class MailLog(BaseModel):
    type: MessageType
    date: datetime = Field(...)
    message: str = Field(...)
    int_id: str = Field(..., max_length=16)
    id: str | None = None
    address: str | None = None

