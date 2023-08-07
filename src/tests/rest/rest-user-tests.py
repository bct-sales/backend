import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.db.database import DatabaseSession
from backend.db import models


def test_list_events_not_logged_in(client: TestClient,
                                   session: DatabaseSession,
                                   sales_event: models.SalesEventCreate):
    response = client.get('/events')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_events_as_seller(client: TestClient,
                               session: DatabaseSession,
                               seller_access_token: str,
                               sales_event: models.SalesEventCreate):
    headers = {'Authorization': f'Bearer {seller_access_token}'}
    response = client.get('/me/items', headers=headers)
    json = response.json()

    assert response.status_code == status.HTTP_200_OK


def test_list_events_as_admin(client: TestClient,
                              session: DatabaseSession,
                              admin_access_token: str,
                              sales_event: models.SalesEventCreate):
    headers = {'Authorization': f'Bearer {admin_access_token}'}
    response = client.get('/me/items', headers=headers)
    json = response.json()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
