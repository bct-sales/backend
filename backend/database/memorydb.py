from backend.database.base import Database
import backend.database.models as models


class InMemoryDatabase(Database):
    __items: list[models.ItemCreate]

    def __init__(self):
        self.__items = [
            models.Item(item_id=1, description='some item', price_in_cents=100),
            models.Item(item_id=2, description='some other item', price_in_cents=200),
        ]

    def list_items(self) -> list[models.Item]:
        return self.__items

    def create_item(self, item: models.ItemCreate) -> int:
        id = self.__generate_unique_item_id()
        new_item = models.Item(**item, id=id)
        self.__items.append(new_item)
        return id
