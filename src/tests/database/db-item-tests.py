import pytest

from backend.db import models, orm
from backend.db.database import DatabaseSession
from backend.db.exceptions import *


@pytest.mark.parametrize('description', [
    'blue shirt',
    'black shirt',
    'white hat',
])
@pytest.mark.parametrize('price_in_cents', [
    50,
    1200
])
def test_create_item(session: DatabaseSession,
                     seller: models.User,
                     sales_event: models.SalesEvent,
                     description: str,
                     price_in_cents: int):
    item_creation = models.ItemCreate(
        description=description,
        price_in_cents=price_in_cents,
        owner_id=seller.user_id,
        recipient_id=seller.user_id,
        sales_event_id=sales_event.sales_event_id,
    )

    item = session.create_item(item=item_creation)

    assert item.description == description
    assert item.owner_id == seller.user_id
    assert item.recipient_id == seller.user_id
    assert item.price_in_cents == price_in_cents
