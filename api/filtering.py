from typing import Annotated, Any

from pydantic import (
    BaseModel,
    Field,
    create_model,
)
from sqlalchemy import ColumnElement, column
from sqlalchemy.sql import operators

from api.db import Model

FILTERING_OPS = {
    'eq': operators.eq,
    'gt': operators.gt,
    'lt': operators.lt,
    'icontains': operators.icontains_op,
}


def resolve_filters(filters: dict[str, Any]) -> list[ColumnElement[Any]]:
    ops: list[ColumnElement[Any]] = []

    for key, value in filters.items():
        field_name, op_name = key.split('__')
        op = FILTERING_OPS[op_name]
        ops.append(op(column(field_name), value))

    return ops


def create_model_filters_schema(model: type[Model]) -> type[BaseModel]:
    defs: dict[str, Any] = {}

    for field in model.__table__.columns:
        for op in FILTERING_OPS:
            defs.update({
                f'{field.name}__{op}': Annotated[
                    field.type.python_type | None,
                    Field(None),
                ]
            })

    return create_model(f'{model.__name__}Filters', **defs)
