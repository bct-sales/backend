import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.database import models
from backend.database.base import DatabaseSession
from backend.security import roles
from tests.conftest import Seller


def test_login(client: TestClient, session: DatabaseSession, seller: Seller):
    payload = {
        'grant_type': 'password',
        'username': seller.email_address,
        'password': seller.password
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = client.post('/login', data=payload, headers=headers)

    assert response.status_code == status.HTTP_200_OK

