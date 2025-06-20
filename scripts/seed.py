#!.venv/bin/python


import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))

import asyncio

from mimesis import Field, Schema
from mimesis.enums import CountryCode
from mimesis.locales import Locale
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import session_factory
from api.models import DataEntry

field = Field(locale=Locale.RU)


def schema_definition() -> dict[str, Field]:
    return {
        'name': field('title'),
        'version': field('version'),
        'desc': field('text', quantity=5),
        'country': field('country_code', code=CountryCode.NUMERIC, key=int),
        'parent': field('integer_number', start=1, end=100_000),
        'count': field('integer_number', start=1, end=100_000),
        'created_at': field('datetime', start=2020, end=2025),
    }


schema = Schema(schema=schema_definition, iterations=1_000)


async def seed_data(db_session: AsyncSession) -> None:
    async with db_session.begin():
        db_session.add_all(DataEntry(**item) for item in iter(schema))


async def main() -> None:
    async with session_factory() as db_session:
        await seed_data(db_session)


if __name__ == '__main__':
    asyncio.run(main())
