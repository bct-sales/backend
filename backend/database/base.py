from abc import ABC, abstractmethod
import backend.database.models as models


class Database(ABC):
    @abstractmethod
    def list_items(self) -> list[models.Item]:
        ...
