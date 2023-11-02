import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.db.database import DatabaseSession
from backend.db import models

from tests.util import Exists


def test_list_events_as_cashier(client: TestClient,
                                session: DatabaseSession,
                                cashier_headers: dict[str, str],
                                items: list[models.Item],
                                items_url: str):
    response = client.get(items_url, headers=cashier_headers)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert 'item_ids' in data
    assert len(data['item_ids']) == len(items)


def test_get_item(client: TestClient,
                  session: DatabaseSession,
                  cashier_headers: dict[str, str],
                  items: list[models.Item],
                  items_url: str):
    for item in items:
        item_url = f"{items_url}{item.item_id}"
        response = client.get(item_url, headers=cashier_headers)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data == {
            'item_id': item.item_id,
            'description': item.description,
            'category': item.category,
            'price_in_cents': item.price_in_cents,
            'recipient_id': item.recipient_id,
            'sales_event_id': item.sales_event_id,
            'owner_id': item.owner_id,
            'charity': item.charity,
            'has_been_sold': False
        }
