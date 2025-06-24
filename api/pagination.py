from abc import ABC, abstractmethod
from base64 import b64decode, b64encode
from math import ceil
from typing import Any, ClassVar, TypedDict, Unpack, override

from sqlakeyset import Page, serialize_bookmark, unserialize_bookmark
from sqlakeyset.asyncio import select_page
from sqlakeyset.types import MarkerLike
from sqlalchemy import (
    Row,
    Select,
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import lazyload

from api.db import Model
from api.utils import get_default_model, get_query_ordering


class PaginationError(Exception):
    pass


class BasePaginatedData[T](TypedDict):
    results: list[T]


class BasePaginationParams[T](TypedDict):
    page_size: int


class BasePaginator(ABC):
    default_error_messages: ClassVar[dict[str, str]] = {
        'invalid_page': 'Такой страницы не существует'
    }

    _db_session: AsyncSession

    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def _get_count(self, query: Select[Any]) -> int:
        subquery = query.options(lazyload('*')).order_by(None).subquery()
        result = await self._db_session.execute(
            select(func.count()).select_from(subquery)
        )
        return result.scalars().one()

    @abstractmethod
    async def paginate[T: Model](
        self, query: Select[Any], **kwargs: Unpack[BasePaginationParams[T]]
    ) -> BasePaginatedData[T]: ...


class PageNumberPaginatedData[T](BasePaginatedData[T]):
    count: int
    next: int | None
    previous: int | None


class PageNumberPaginationParams[T](BasePaginationParams[T]):
    page: int


class PageNumberPaginator(BasePaginator):
    @override
    async def paginate[T: Model](
        self,
        query: Select[Any],
        **kwargs: Unpack[PageNumberPaginationParams[T]],
    ) -> PageNumberPaginatedData[T]:
        page, page_size = kwargs['page'], kwargs['page_size']

        if (
            model := get_default_model(query)
        ) is not None and not get_query_ordering(query):
            query = query.order_by(model.pk.asc())

        count = await self._get_count(query)
        total_pages = ceil(count / page_size) if count != 0 else 0

        if page > total_pages or page < 1:
            raise PaginationError(self.default_error_messages['invalid_page'])

        next_page = page + 1 if page < total_pages else None
        previous_page = (
            total_pages
            if page > total_pages
            else page - 1
            if page > 1
            else None
        )

        results = list(
            (
                await self._db_session.execute(
                    query.limit(page_size).offset(page_size * (page - 1))
                )
            )
            .scalars()
            .all()
        )

        return PageNumberPaginatedData[T](
            results=results,
            count=count,
            next=next_page,
            previous=previous_page,
        )


class CursorPaginatedData[T](BasePaginatedData[T]):
    next: str | None
    previous: str | None


class CursorPaginationParams[T](BasePaginationParams[T]):
    cursor: str | None


def _decode_cursor(encoded: str | None) -> MarkerLike:
    if encoded is None:
        return (None, False)
    return unserialize_bookmark(b64decode(encoded.encode()).decode())


def _encode_cursor(cursor: MarkerLike) -> str:
    return b64encode(serialize_bookmark(cursor).encode()).decode()


class CursorPaginator(BasePaginator):
    default_error_messages: ClassVar[dict[str, str]] = {
        **BasePaginator.default_error_messages,
        'invalid_cursor': 'Невалидный курсор',
    }

    @override
    async def paginate[T: Model](
        self, query: Select[Any], **kwargs: Unpack[CursorPaginationParams[T]]
    ) -> CursorPaginatedData[T]:
        encoded_cursor, page_size = kwargs['cursor'], kwargs['page_size']

        try:
            cursor = _decode_cursor(encoded_cursor)
        except ValueError as exc:
            raise PaginationError(
                self.default_error_messages['invalid_cursor']
            ) from exc

        if (
            model := get_default_model(query)
        ) is not None and not get_query_ordering(query):
            query = query.order_by(model.pk.asc())

        page: Page[Row[tuple[T, int]]] = await select_page(
            self._db_session, query, per_page=page_size, page=cursor
        )

        return CursorPaginatedData(
            results=[row[0] for row in page.paging.rows],
            next=_encode_cursor(page.paging.next)
            if page.paging.has_next
            else None,
            previous=_encode_cursor(page.paging.previous)
            if page.paging.has_previous
            else None,
        )
