from collections.abc import Mapping
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import Model
from api.pagination import PageNumberPaginatedData, PageNumberPaginator


class Repository[T: Model]:
    model: type[T]

    _db_session: AsyncSession

    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def page_number_paginated_list(
        self,
        *,
        page: int,
        page_size: int,
    ) -> PageNumberPaginatedData[T]:
        query = select(self.model, self.model.pk)

        paginator = PageNumberPaginator(self._db_session)

        return await paginator.paginate(query, page_size=page_size, page=page)

    async def create(self, **kwargs: Mapping[str, Any]) -> T:
        instance = self.model(**kwargs)
        self._db_session.add(instance)
        await self._db_session.commit()
        await self._db_session.refresh(instance)
        return instance
