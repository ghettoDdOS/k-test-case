from sqlalchemy import SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from api.db import Model, TimeStampMixin


class DataEntry(TimeStampMixin, Model):
    name: Mapped[str] = mapped_column(String(length=255))
    version: Mapped[str] = mapped_column(String(length=50))
    desc: Mapped[str] = mapped_column(Text())
    country: Mapped[int] = mapped_column(SmallInteger())
    count: Mapped[int]
    parent: Mapped[int]
