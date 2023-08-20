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


@pytest.mark.parametrize('description', [
    'blue shirt',
    'black shirt',
    'white hat',
])
@pytest.mark.parametrize('price_in_cents', [
    50,
    1200
])
def test_find_item(session: DatabaseSession,
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

    orm_item = session.create_item(item=item_creation)
    item = session.find_item_by_id(orm_item.item_id)

    assert item is not None
    assert item.description == description
    assert item.owner_id == seller.user_id
    assert item.recipient_id == seller.user_id
    assert item.price_in_cents == price_in_cents


@pytest.mark.parametrize('description', [
    'blue shirt',
    'black shirt',
    'white hat',
])
@pytest.mark.parametrize('price_in_cents', [
    50,
    1200
])
def test_list_items(session: DatabaseSession,
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

    orm_item = session.create_item(item=item_creation)
    items = session.list_items()

    assert len(items) == 1
    item = items[0]

    assert item is not None
    assert item.description == description
    assert item.owner_id == seller.user_id
    assert item.recipient_id == seller.user_id
    assert item.price_in_cents == price_in_cents


@pytest.mark.parametrize('description', [
    'blue shirt',
    'black shirt',
    'white hat',
])
@pytest.mark.parametrize('price_in_cents', [
    50,
    1200
])
def test_delete_item(session: DatabaseSession,
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

    orm_item = session.create_item(item=item_creation)
    session.delete_item_by_id(orm_item.item_id)

    items = session.list_items()

    assert len(items) == 0
