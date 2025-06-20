from fastapi import HTTPException, status

from api.db import Model
from api.pagination import PaginationError
from api.repositories.base import Repository
from api.schemas import (
    CursorPaginatedResponseSchema,
    CursorPaginationParamsSchema,
    ModelSchema,
    PageNumberPaginatedResponseSchema,
    PageNumberPaginationParamsSchema,
)


class DatabaseService[T: Model]:
    def __init__(self, repository: Repository[T]) -> None:
        self._repository = repository

    async def page_number_paginated_list[S: ModelSchema](
        self,
        schema: type[S],
        pagination_params: PageNumberPaginationParamsSchema,
    ) -> PageNumberPaginatedResponseSchema[S]:
        try:
            data = await self._repository.page_number_paginated_list(
                page=pagination_params.page,
                page_size=pagination_params.page_size,
            )
        except PaginationError as exc:
            raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
        else:
            return PageNumberPaginatedResponseSchema[S](
                results=[
                    schema.model_validate(item) for item in data['results']
                ],
                count=data['count'],
                next=data['next'],
                previous=data['previous'],
            )

    async def cursor_paginated_list[S: ModelSchema](
        self,
        schema: type[S],
        pagination_params: CursorPaginationParamsSchema,
    ) -> CursorPaginatedResponseSchema[S]:
        try:
            data = await self._repository.cursor_paginated_list(
                cursor=pagination_params.cursor,
                page_size=pagination_params.page_size,
            )
        except PaginationError as exc:
            raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
        else:
            return CursorPaginatedResponseSchema[S](
                results=[
                    schema.model_validate(item) for item in data['results']
                ],
                next=data['next'],
                previous=data['previous'],
            )

    async def create[S: ModelSchema](
        self, schema: type[S], model: ModelSchema
    ) -> S:
        instance = await self._repository.create(**model.model_dump())
        return schema.model_validate(instance)
