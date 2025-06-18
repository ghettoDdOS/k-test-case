from collections.abc import Mapping
from typing import Any

from api.db import Model
from api.pagination import Cursor
from api.repositories.base import Repository
from api.schemas import ModelSchema, PaginatedResponseSchema


class DatabaseService[T: Model, R: Repository]:
    def __init__(self, repository: R) -> None:
        self._repository = repository

    async def list[S: ModelSchema](
        self,
        schema: type[S],
        *,
        page_size: int,
        cursor: Cursor | None = None,
    ) -> PaginatedResponseSchema[S]:
        paginator = await self._repository.list(
            cursor=cursor, page_size=page_size
        )

        return PaginatedResponseSchema(
            results=[
                schema.model_validate(item) for item in paginator.results
            ],
            next=paginator.next,
            previous=paginator.previous,
        )

    async def create[S: ModelSchema](
        self, schema: type[S], /, **kwargs: Mapping[str, Any]
    ) -> S:
        obj = await self._repository.create(**kwargs)
        return schema.model_validate(obj)
