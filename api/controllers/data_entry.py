from typing import Annotated

from fastapi import APIRouter, Query

from api.deps import DataEntryServiceDep
from api.schemas import (
    CursorPaginatedResponseSchema,
    DataEntryCreateSchema,
    DataEntryCursorPaginatedListParams,
    DataEntryPageNumberPaginatedListParams,
    DataEntrySchema,
    PageNumberPaginatedResponseSchema,
)

router = APIRouter(tags=['data_entry'])


@router.get('/page-number-paginated')
async def data_entry_page_number_paginated_list(
    service: DataEntryServiceDep,
    params: Annotated[DataEntryPageNumberPaginatedListParams, Query()],
) -> PageNumberPaginatedResponseSchema[DataEntrySchema]:
    return await service.page_number_paginated_list(DataEntrySchema, params)


@router.get('/cursor-paginated')
async def data_entry_cursor_paginated_list(
    service: DataEntryServiceDep,
    params: Annotated[DataEntryCursorPaginatedListParams, Query()],
) -> CursorPaginatedResponseSchema[DataEntrySchema]:
    return await service.cursor_paginated_list(DataEntrySchema, params)


@router.post('/')
async def data_entry_create(
    service: DataEntryServiceDep, data: DataEntryCreateSchema
) -> DataEntrySchema:
    return await service.create(DataEntrySchema, data)
