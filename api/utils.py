from alembic.environment import Any
from sqlalchemy import ColumnElement, Select

from api.db import Model


def get_query_models(query: Select[Any]) -> set[type[Model]]:
    return {col_desc['entity'] for col_desc in query.column_descriptions}


def get_default_model(query: Select[Any]) -> type[Model] | None:
    query_models = get_query_models(query)
    if len(query_models) == 1:
        (default_model,) = iter(query_models)
    else:
        default_model = None
    return default_model


def get_query_ordering(query: Select[Any]) -> tuple[ColumnElement[Any], ...]:
    return query._order_by_clauses  # type: ignore [has no alternatives]  # noqa: SLF001
