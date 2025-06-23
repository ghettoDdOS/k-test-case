from typing import Any, ClassVar

from fastapi import HTTPException, status
from sqlalchemy import (
    ColumnExpressionArgument,
    UnaryExpression,
    asc,
    desc,
)

from api.db import Model
from api.pagination import PaginationError
from api.repositories.base import Repository
from api.schemas import (
    CommonCursorPaginatedParams,
    CommonPageNumberPaginatedParams,
    CursorPaginatedResponseSchema,
    ModelSchema,
    PageNumberPaginatedResponseSchema,
)


class DatabaseService[T: Model]:
    default_error_messages: ClassVar[dict[str, str]] = {
        'invalid_ordering_key': 'Ошибка сортировки: столбца "%s" не существует'
    }

    def __init__(self, repository: Repository[T]) -> None:
        self._repository = repository

    def _validate_model_field(
        self, field_name: str
    ) -> ColumnExpressionArgument[Any]:
        col = self._repository.model.__table__.columns.get(field_name)
        if col is None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                self.default_error_messages['invalid_ordering_key']
                % field_name,
            )
        return col

    def _validate_ordering_params(
        self,
        ordering: list[str],
    ) -> list[UnaryExpression[Any]]:
        clauses: list[UnaryExpression[Any]] = []
        for key in ordering:
            if key.startswith('-'):
                clauses.append(desc(self._validate_model_field(key[1:])))
            else:
                clauses.append(asc(self._validate_model_field(key)))

        return clauses

    async def page_number_paginated_list[S: ModelSchema](
        self, schema: type[S], params: CommonPageNumberPaginatedParams
    ) -> PageNumberPaginatedResponseSchema[S]:
        page_size, page, ordering = (
            params.page_size,
            params.page,
            params.ordering,
        )
        filters = params.model_dump(
            exclude_unset=True,
            exclude=set(CommonPageNumberPaginatedParams.model_fields.keys()),
        )

        ordering_clauses = (
            self._validate_ordering_params(ordering) if ordering else None
        )
        try:
            data = await self._repository.page_number_paginated_list(
                page=page,
                page_size=page_size,
                ordering=ordering_clauses,
                filters=filters,
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
        params: CommonCursorPaginatedParams,
    ) -> CursorPaginatedResponseSchema[S]:
        page_size, cursor, ordering = (
            params.page_size,
            params.cursor,
            params.ordering,
        )
        filters = params.model_dump(
            exclude_unset=True,
            exclude=set(CommonCursorPaginatedParams.model_fields.keys()),
        )

        ordering_clauses = (
            self._validate_ordering_params(ordering) if ordering else None
        )
        try:
            data = await self._repository.cursor_paginated_list(
                cursor=cursor,
                page_size=page_size,
                ordering=ordering_clauses,
                filters=filters,
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
