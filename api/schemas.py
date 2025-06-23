from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from api.filtering import create_model_filters_schema
from api.models import DataEntry


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


class BasePaginationParamsSchema(BaseModel):
    page_size: Annotated[int, Field(ge=10, le=1000)] = 100


class PageNumberPaginationParamsSchema(BasePaginationParamsSchema):
    page: Annotated[int, Field(ge=1)] = 1


class CursorPaginationParamsSchema(BasePaginationParamsSchema):
    cursor: str | None = None


class BasePaginationResponseSchema[T](BaseModel):
    results: list[T]


class PageNumberPaginatedResponseSchema[T](BasePaginationResponseSchema[T]):
    count: int
    next: int | None
    previous: int | None


class CursorPaginatedResponseSchema[T](BasePaginationResponseSchema[T]):
    next: str | None
    previous: str | None


class OrderingParamsSchema(BaseModel):
    ordering: list[str] | None = None


class CommonPageNumberPaginatedParams(
    OrderingParamsSchema, PageNumberPaginationParamsSchema
):
    pass


class CommonCursorPaginatedParams(
    OrderingParamsSchema, CursorPaginationParamsSchema
):
    pass


DataEntryFiltersSchema = create_model_filters_schema(DataEntry)


class DataEntryPageNumberPaginatedListParams(
    CommonPageNumberPaginatedParams, DataEntryFiltersSchema
):
    pass


class DataEntryCursorPaginatedListParams(
    CommonCursorPaginatedParams, DataEntryFiltersSchema
):
    pass
