from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column


class TimeStampMixin:
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())


class CommonMixin:
    id: Mapped[int] = mapped_column(primary_key=True)

