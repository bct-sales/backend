import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.db.database import DatabaseSession
from backend.db import models

from tests.util import Exists


@pytest.mark.parametrize('sold_item_ids', [
    [1],
    [1, 2],
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
