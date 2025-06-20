from abc import ABC, abstractmethod
from math import ceil
from typing import Any, ClassVar, TypedDict, Unpack, override

from sqlalchemy import Select, func, select
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

    @abstractmethod
    async def _get_count(self, query: Select[Any]) -> int: ...

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
    async def _get_count(self, query: Select[Any]) -> int:
        return (
            (
                await self._db_session.execute(
                    select(func.count()).select_from(
                        query.options(lazyload('*')).order_by(None).subquery()
                    )
                )
            )
            .scalars()
            .one()
        )

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
