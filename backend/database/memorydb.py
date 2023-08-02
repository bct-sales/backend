from backend.database.base import Database
import backend.database.models as models


class InMemoryDatabase(Database):
    def list_items(self):
        return [
            models.Item(description='some item', price_in_cents=100),
            models.Item(description='some other item', price_in_cents=200),
        ]
