import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.db.database import DatabaseSession
from backend.db import models


def test_list_items_not_logged_in(client: TestClient,
                                   session: DatabaseSession,
                                   sales_event: models.SalesEventCreate):
    response = client.get('/me/items')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_items_as_seller(client: TestClient,
                              session: DatabaseSession,
                              seller_headers: dict[str, str],
                              sales_event: models.SalesEventCreate):
    response = client.get('/me/items', headers=seller_headers)
    json = response.json()

    assert response.status_code == status.HTTP_200_OK


def test_list_items_as_admin(client: TestClient,
                             session: DatabaseSession,
                             admin_headers: dict[str, str],
                             sales_event: models.SalesEventCreate):
    response = client.get('/me/items', headers=admin_headers)
    json = response.json()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
