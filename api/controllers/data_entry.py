from fastapi import APIRouter

from api.deps import CursorDep, DataEntryServiceDep
from api.schemas import (
    DataEntryCreateSchema,
    DataEntrySchema,
    PaginatedResponseSchema,
)

router = APIRouter(tags=['data_entry'])


@router.get('/')
async def data_entry_list(
    service: DataEntryServiceDep, cursor: CursorDep, page_size: int = 100
) -> PaginatedResponseSchema[DataEntrySchema]:
    return await service.list(
        DataEntrySchema, cursor=cursor, page_size=page_size
    )


@router.post('/')
async def data_entry_create(
    service: DataEntryServiceDep, data: DataEntryCreateSchema
) -> DataEntrySchema:
    return await service.create(DataEntrySchema, **data.model_dump())
