from collections.abc import Generator, Mapping, Sequence
from datetime import date, datetime
from typing import Any

from sqlalchemy import Integer, UnaryExpression, asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import asc_op, desc_op

from api.db import Model
from api.pagination import Cursor, Paginator


def _reverse_ordering(
    *expressions: UnaryExpression[Any],
) -> Generator[UnaryExpression[Any]]:
    for exp in expressions:
        if exp.modifier is desc_op:
            yield asc(exp.element)
        elif exp.modifier is asc_op:
            yield desc(exp.element)


def _get_position_from_item(
    item: Model, ordering: Sequence[UnaryExpression[Any]]
) -> str:
    field = ordering[0].element
    return str(getattr(item, field.key))


def _get_next_cursor(
    page: list[Model],
    cursor: Cursor,
    next_position: str | None,
    previous_position: str | None,
    ordering: Sequence[UnaryExpression[Any]],
    page_size: int,
) -> str | None:
    if next_position is None:
        return None

    if page and cursor.reverse and cursor.offset != 0:
        compare = _get_position_from_item(page[-1], ordering)
    else:
        compare = next_position
    offset = 0

    has_item_with_unique_position = False
    for item in reversed(page):
        position = _get_position_from_item(item, ordering)
        if position != compare:
            has_item_with_unique_position = True
            break

        compare = position
        offset += 1

    if page and not has_item_with_unique_position:
        if previous_position is None:
            offset = page_size
            position = None
        elif cursor.reverse:
            offset = 0
            position = previous_position
        else:
            offset = cursor.offset + page_size
            position = previous_position

    if not page:
        position = next_position

    return Cursor(offset=offset, reverse=False, position=position).encode()


def _get_previous_cursor(
    page: list[Model],
    cursor: Cursor,
    next_position: str | None,
    previous_position: str | None,
    ordering: Sequence[UnaryExpression[Any]],
    page_size: int,
) -> str | None:
    if previous_position is None:
        return None

    if page and not cursor.reverse and cursor.offset != 0:
        compare = _get_position_from_item(page[0], ordering)
    else:
        compare = previous_position
    offset = 0

    has_item_with_unique_position = False
    for item in page:
        position = _get_position_from_item(item, ordering)
        if position != compare:
            has_item_with_unique_position = True
            break

        compare = position
        offset += 1

    if page and not has_item_with_unique_position:
        if next_position is None:
            offset = page_size
            position = None
        elif cursor.reverse:
            offset = cursor.offset + page_size
            position = next_position
        else:
            offset = 0
            position = next_position

    if not page:
        position = previous_position

    return Cursor(offset=offset, reverse=True, position=position).encode()


def to_python[T](python_type: T, value: str) -> T:
    if python_type is str:
        return value

    if python_type is int:
        return int(value)

    if python_type is datetime:
        return datetime.fromisoformat(value)

    msg = 'Invalid data type'
    raise ValueError(msg)


class Repository[T: Model]:
    model: type[T]

    _db_session: AsyncSession

    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def list(
        self,
        *,
        page_size: int,
        cursor: Cursor | None = None,
        ordering: Sequence[UnaryExpression[Any]] | None = None,
    ) -> Paginator[T]:
        query = select(self.model)

        if cursor is None:
            cursor = Cursor(offset=0, reverse=False, position=None)

        if not ordering:
            ordering = (self.model.pk.desc(),)

        if not cursor.reverse:
            query = query.order_by(*_reverse_ordering(*ordering))
        else:
            query = query.order_by(*ordering)

        if cursor.position is not None:
            order = ordering[0]
            is_reversed = order.modifier is desc_op
            order_attr = order.element

            compare = to_python(order_attr.type.python_type, cursor.position)
            if cursor.reverse != is_reversed:
                query = query.where(order_attr < compare)
            else:
                query = query.where(order_attr > compare)

        query = query.offset(cursor.offset).limit(page_size + 1)

        results = (await self._db_session.execute(query)).scalars().all()
        page = list(results[:page_size])

        if len(results) > len(page):
            has_following_position = True
            order_attr = ordering[0].element
            following_position = _get_position_from_item(results[-1], ordering)
        else:
            has_following_position = False
            following_position = None

        next_position = None
        previous_position = None
        if cursor.reverse:
            page.reverse()

            has_next = (cursor.position is not None) or (cursor.offset > 0)
            has_previous = has_following_position
            if has_next:
                next_position = cursor.position
            if has_previous:
                previous_position = following_position

        else:
            has_next = has_following_position
            has_previous = (cursor.position is not None) or (cursor.offset > 0)
            if has_next:
                next_position = following_position
            if has_previous:
                previous_position = cursor.position

        return Paginator(
            results=page,
            next=_get_next_cursor(
                page,
                cursor,
                next_position,
                previous_position,
                ordering,
                page_size,
            ),
            previous=_get_previous_cursor(
                page,
                cursor,
                next_position,
                previous_position,
                ordering,
                page_size,
            ),
        )

    async def create(self, **kwargs: Mapping[str, Any]) -> T:
        instance = self.model(**kwargs)
        self._db_session.add(instance)
        await self._db_session.commit()
        await self._db_session.refresh(instance)
        return instance
