import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.db.database import DatabaseSession
from tests.conftest import User


def test_login(client: TestClient, session: DatabaseSession, seller: User):
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


def test_login_with_nonexisting_email_address(client: TestClient, session: DatabaseSession, valid_email_address: str, valid_password):
    payload = {
        'grant_type': 'password',
        'username': valid_email_address,
        'password': valid_password,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = client.post('/login', data=payload, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_with_wrong_password(client: TestClient, session: DatabaseSession, seller: User, valid_password):
    payload = {
        'grant_type': 'password',
        'username': seller.email_address,
        'password': valid_password,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = client.post('/login', data=payload, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
