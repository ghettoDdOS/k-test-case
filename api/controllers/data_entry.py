from collections.abc import Sequence

from fastapi import APIRouter

from api.deps import DataEntryServiceDep
from api.models import DataEntry
from api.schemas import DataEntryCreateSchema, DataEntrySchema

router = APIRouter(tags=['data_entry'])


@router.get('/', response_model=list[DataEntrySchema])
async def data_entry_list(service: DataEntryServiceDep) -> Sequence[DataEntry]:
    return await service.list()


@router.post('/', response_model=DataEntrySchema)
async def data_entry_create(
    service: DataEntryServiceDep, data: DataEntryCreateSchema
) -> DataEntry:
    return await service.create(**data.model_dump())
