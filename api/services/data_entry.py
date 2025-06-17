from api.models import DataEntry
from api.repositories.data_entry import DataEntryRepository
from api.services.base import DatabaseService


class DataEntryService(DatabaseService[DataEntry, DataEntryRepository]):
    pass
