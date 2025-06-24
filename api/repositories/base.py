from collections.abc import Mapping, Sequence
from typing import Any

from sqlalchemy import Select, UnaryExpression, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import Model
from api.filtering import resolve_filters
from api.pagination import (
    CursorPaginatedData,
    CursorPaginator,
    PageNumberPaginatedData,
    PageNumberPaginator,
)


def apply_ordering(
    query: Select[Any],
    ordering: Sequence[UnaryExpression[Any]] | None = None,
) -> Select[Any]:
    if not ordering:
        return query
    return query.order_by(*ordering)


def apply_filters(
    query: Select[Any],
    filters: dict[str, Any] | None = None,
) -> Select[Any]:
    if not filters:
        return query
    clauses = resolve_filters(filters)
    return query.where(*clauses)


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
        ordering: Sequence[UnaryExpression[Any]] | None = None,
        filters: dict[str, Any] | None = None,
    ) -> PageNumberPaginatedData[T]:
        query = apply_ordering(
            apply_filters(select(self.model), filters), ordering
        )

        paginator = PageNumberPaginator(self._db_session)

        return await paginator.paginate(query, page_size=page_size, page=page)

    async def cursor_paginated_list(
        self,
        *,
        cursor: str | None,
        page_size: int,
        ordering: Sequence[UnaryExpression[Any]] | None = None,
        filters: dict[str, Any] | None = None,
    ) -> CursorPaginatedData[T]:
        query = apply_ordering(
            apply_filters(select(self.model), filters), ordering
        )

        paginator = CursorPaginator(self._db_session)

        return await paginator.paginate(
            query, page_size=page_size, cursor=cursor
        )

    async def create(self, **kwargs: Mapping[str, Any]) -> T:
        instance = self.model(**kwargs)
        self._db_session.add(instance)
        await self._db_session.commit()
        await self._db_session.refresh(instance)
        return instance
