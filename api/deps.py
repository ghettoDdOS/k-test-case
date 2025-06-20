from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import session_factory
from api.repositories import DataEntryRepository
from api.services import DataEntryService


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session


DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def get_data_entry_service(db_session: DbSessionDep) -> DataEntryService:
    repo = DataEntryRepository(db_session)
    return DataEntryService(repo)


DataEntryServiceDep = Annotated[
    DataEntryService, Depends(get_data_entry_service)
]
