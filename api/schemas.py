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
