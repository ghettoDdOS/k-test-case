from collections.abc import Sequence
from typing import Any

from sqlalchemy import UnaryExpression

from api.models import DataEntry
from api.pagination import Cursor, Paginator
from api.repositories.base import Repository


class DataEntryRepository(Repository[DataEntry]):
    model = DataEntry

    async def list(
        self,
        *,
        page_size: int,
        cursor: Cursor | None = None,
        ordering: Sequence[UnaryExpression[Any]] | None = None,
    ) -> Paginator[DataEntry]:
        if not ordering:
            ordering = (DataEntry.created_at.desc(),)
        return await super().list(
            page_size=page_size, cursor=cursor, ordering=ordering
        )
