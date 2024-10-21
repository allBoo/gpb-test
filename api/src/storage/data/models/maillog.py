import uuid
from datetime import datetime

from sqlalchemy import types, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from shared.data.db.model import BaseModel


class Message(BaseModel):
    id: Mapped[str] = mapped_column(types.String, nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    int_id: Mapped[str] = mapped_column(types.String(length=16), nullable=False, index=True)
    created: Mapped[datetime] = mapped_column(types.DateTime, nullable=False, index=True)
    str: Mapped[str] = mapped_column(types.String, nullable=False)
    status: Mapped[bool] = mapped_column(types.Boolean, default=True)


class Log(BaseModel):
    int_id: Mapped[str] = mapped_column(types.String(length=16), nullable=False, index=True)
    created: Mapped[datetime] = mapped_column(types.DateTime, nullable=False)
    str: Mapped[str | None] = mapped_column(types.String, nullable=True)
    address: Mapped[str | None] = mapped_column(types.String, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('int_id', 'created', 'str'),
        {'extend_existing': True}
    )
