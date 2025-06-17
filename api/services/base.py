from collections.abc import Mapping, Sequence
from typing import Any

from api.db import Model
from api.repositories.base import Repository


class DatabaseService[T: Model, R: Repository]:
    def __init__(self, repository: R) -> None:
        self._repository = repository

    async def list(self) -> Sequence[T]:
        return await self._repository.list()

    async def create(self, **kwargs: Mapping[str, Any]) -> T:
        return await self._repository.create(**kwargs)
