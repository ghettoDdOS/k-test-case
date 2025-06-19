from datetime import datetime

from pydantic.alias_generators import to_snake
from sqlalchemy import func
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

from api.config import settings

engine = create_async_engine(
    str(settings.DATABASE_URL), echo=settings.QUERY_LOGGER
)

session_factory = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False
)


class Model(AsyncAttrs, DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return to_snake(cls.__name__)

    pk: Mapped[int] = mapped_column(primary_key=True)


class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(default=func.now())
