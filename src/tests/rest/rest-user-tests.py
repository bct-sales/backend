import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.db.database import DatabaseSession
from backend.db import models


def test_list_items_not_logged_in(client: TestClient,
                                  sales_event: models.SalesEvent,
                                  session: DatabaseSession):
    url = f'/api/v1/me/events/{sales_event.sales_event_id}/items'
    response = client.get(url=url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_items_as_seller(client: TestClient,
                              session: DatabaseSession,
                              sales_event: models.SalesEvent,
                              seller_headers: dict[str, str]):
    url = f'/api/v1/me/events/{sales_event.sales_event_id}/items'
    response = client.get(url=url, headers=seller_headers)
    json = response.json()

    assert response.status_code == status.HTTP_200_OK
    # TODO


def test_list_items_as_admin(client: TestClient,
                             session: DatabaseSession,
                             sales_event: models.SalesEvent,
                             admin_headers: dict[str, str]):
    url = f'/api/v1/me/events/{sales_event.sales_event_id}/items'
    response = client.get(url=url, headers=admin_headers)

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
    url = '/api/v1/me/items'
    response = client.post(url=url, headers=admin_headers, json=payload)

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
    url = '/api/v1/me/items'
    response = client.post(url=url, headers=seller_headers, json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    response_item = models.Item.model_validate_json(response.read())
    assert response_item.description == description
    assert response_item.price_in_cents == price_in_cents
    assert response_item.owner_id == seller.user_id
    assert response_item.recipient_id == recipient_id
    assert response_item.sales_event_id == sales_event_id

    items_in_database = session.list_items()
    assert len(items_in_database) == 1
    item_in_database = items_in_database[0]
    assert item_in_database.description == description
    assert item_in_database.price_in_cents == price_in_cents
    assert item_in_database.owner_id == seller.user_id
    assert item_in_database.recipient_id == recipient_id
    assert item_in_database.sales_event_id == sales_event_id


def test_add_item_as_seller_missing_fields(client: TestClient,
                                           session: DatabaseSession,
                                           seller: models.User,
                                           seller_headers: dict[str, str],
                                           sales_event: models.SalesEvent):
    payload = {
        'description': 'blue jeans',
        'price_in_cents': 2000,
        'recipient_id': seller.user_id,
    }
    url = '/api/v1/me/items'
    response = client.post(url=url, headers=seller_headers, json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
