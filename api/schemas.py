from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class ModelSchema(BaseModel):
    model_config = {'from_attributes': True, 'validate_by_alias': False}


class BaseDataEntrySchema(ModelSchema):
    name: str
    version: str
    desc: str
    country: int
    count: int
    parent: int


class DataEntrySchema(BaseDataEntrySchema):
    pk: Annotated[int, Field(alias='id')]
    created_at: datetime


class DataEntryCreateSchema(BaseDataEntrySchema):
    pass


class PageNumberPaginationParamsSchema(BaseModel):
    page: Annotated[int, Field(ge=1)] = 1
    page_size: Annotated[int, Field(ge=10, le=1000)] = 100


class BasePaginationResponseSchema[T](BaseModel):
    results: list[T]


class PageNumberPaginatedResponseSchema[T](BasePaginationResponseSchema[T]):
    count: int
    next: int | None
    previous: int | None
