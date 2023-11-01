import pytest

from backend.db import models, orm
from backend.db.database import DatabaseSession
from backend.db.exceptions import *



@pytest.mark.parametrize("item_selection", [
    (1, ),
    (1, 2),
    (1, 2, 3, 4, 5),
    (5, 6, 7, 8, 9)
])
def test_create_sale(session: DatabaseSession,
                     items: list[models.Item],
                     item_selection: list[int]):
    sale_orm = session.create_sale(item_selection)
    assert set(item.item_id for item in sale_orm.items_sold) == set(item_selection)
