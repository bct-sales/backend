import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.db.database import DatabaseSession
from backend.db import models


def test_list_items_not_logged_in(client: TestClient,
                                   session: DatabaseSession):
    response = client.get('/me/items')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_items_as_seller(client: TestClient,
                              session: DatabaseSession,
                              seller_headers: dict[str, str]):
    response = client.get('/me/items', headers=seller_headers)
    json = response.json()

    assert response.status_code == status.HTTP_200_OK


def test_list_items_as_admin(client: TestClient,
                             session: DatabaseSession,
                             admin_headers: dict[str, str]):
    response = client.get('/me/items', headers=admin_headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_add_item_as_admin(client: TestClient,
                           session: DatabaseSession,
                           admin: models.User,
                           admin_headers: dict[str, str],
                           sales_event: models.SalesEvent):
    payload = {
        'description': 'blue jeans',
        'price_in_cents': 2000,
        'recipient_id': admin.user_id,
        'sales_event_id': sales_event.sales_event_id,
    }
    response = client.post('/me/items', headers=admin_headers, json=payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize('description', [
    'blue jeans',
    'white t-shirt',
    'cowboy boots',
])
@pytest.mark.parametrize('price_in_cents', [
    0,
    100,
    1000,
    5000,
])
def test_add_item_as_seller(client: TestClient,
                            session: DatabaseSession,
                            seller: models.User,
                            seller_headers: dict[str, str],
                            sales_event: models.SalesEvent,
                            description: str,
                            price_in_cents: int):
    recipient_id = seller.user_id
    sales_event_id = sales_event.sales_event_id
    payload = {
        'description': description,
        'price_in_cents': price_in_cents,
        'recipient_id': recipient_id,
        'sales_event_id': sales_event_id,
    }
    response = client.post('/me/items', headers=seller_headers, json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    item = models.Item.model_validate_json(response.read())
    assert item.description == description
    assert item.price_in_cents == price_in_cents
    assert item.owner_id == seller.user_id
    assert item.recipient_id == recipient_id
    assert item.sales_event_id == sales_event_id
