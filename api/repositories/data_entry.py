from api.models import DataEntry
from api.repositories.base import Repository


class DataEntryRepository(Repository[DataEntry]):
    model = DataEntry
