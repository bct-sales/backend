import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.db.database import DatabaseSession
from backend.db import models

from tests.util import Exists


@pytest.mark.parametrize('sold_item_ids', [
    [1],
    [1, 2],
    [1, 3, 4],
    [4, 9, 15, 19]
])
def test_create_sale_as_cashier(client: TestClient,
                                session: DatabaseSession,
                                cashier_headers: dict[str, str],
                                sales_url: str,
                                sold_item_ids: list[int],
                                items: list[models.Item]):
    payload = {
        'item_ids': sold_item_ids,
    }
    response = client.post(sales_url, json=payload, headers=cashier_headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert set(sold_item_ids) ==  set(session.collect_sold_items())
    assert len(sold_item_ids) == len(session.collect_sold_items())


def test_create_sale_with_zero_items(client: TestClient,
                                     session: DatabaseSession,
                                     cashier_headers: dict[str, str],
                                     sales_url: str,
                                     items: list[models.Item]):
    payload = {
        'item_ids': [],
    }
    response = client.post(sales_url, json=payload, headers=cashier_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_sale_with_duplicate_items(client: TestClient,
                                          session: DatabaseSession,
                                          cashier_headers: dict[str, str],
                                          sales_url: str,
                                          items: list[models.Item]):
    payload = {
        'item_ids': [items[0].item_id, items[0].item_id],
    }
    response = client.post(sales_url, json=payload, headers=cashier_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
