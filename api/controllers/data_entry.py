from typing import Annotated

from fastapi import APIRouter, Query

from api.deps import DataEntryServiceDep
from api.schemas import (
    CursorPaginatedResponseSchema,
    CursorPaginationParamsSchema,
    DataEntryCreateSchema,
    DataEntrySchema,
    PageNumberPaginatedResponseSchema,
    PageNumberPaginationParamsSchema,
)

router = APIRouter(tags=['data_entry'])


@router.get('/page-number-paginated')
async def data_entry_page_number_paginated_list(
    service: DataEntryServiceDep,
    page_number_pagination: Annotated[
        PageNumberPaginationParamsSchema, Query()
    ],
) -> PageNumberPaginatedResponseSchema[DataEntrySchema]:
    return await service.page_number_paginated_list(
        DataEntrySchema, page_number_pagination
    )


@router.get('/cursor-paginated')
async def data_entry_cursor_paginated_list(
    service: DataEntryServiceDep,
    cursor_pagination: Annotated[CursorPaginationParamsSchema, Query()],
) -> CursorPaginatedResponseSchema[DataEntrySchema]:
    return await service.cursor_paginated_list(
        DataEntrySchema, cursor_pagination
    )


@router.post('/')
async def data_entry_create(
    service: DataEntryServiceDep, data: DataEntryCreateSchema
) -> DataEntrySchema:
    return await service.create(DataEntrySchema, data)
