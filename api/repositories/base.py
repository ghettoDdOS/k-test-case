from collections.abc import Mapping, Sequence
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import Model


class Repository[T: Model]:
    model: type[T]

    _db_session: AsyncSession

    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def list(self) -> Sequence[T]:
        query = select(self.model)
        result = await self._db_session.execute(query)
        return result.scalars().all()

    async def create(self, **kwargs: Mapping[str, Any]) -> T:
        instance = self.model(**kwargs)
        self._db_session.add(instance)
        await self._db_session.commit()
        await self._db_session.refresh(instance)
        return instance
