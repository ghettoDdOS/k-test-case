from api.models import DataEntry
from api.services.base import DatabaseService


class DataEntryService(DatabaseService[DataEntry]):
    pass
