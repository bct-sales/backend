import pytest
from fastapi import status
from fastapi.testclient import TestClient
from backend.db import models, orm

from backend.db.database import DatabaseSession



def test_login(client: TestClient,
               session: DatabaseSession,
               seller: models.User,
               login_url: str,
               seller_password: str):
    payload = {
        'grant_type': 'password',
        'username': str(seller.user_id),
        'password': seller_password
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = client.post(login_url, data=payload, headers=headers)

    assert response.status_code == status.HTTP_200_OK


def test_login_with_nonexisting_id(client: TestClient,
                                   session: DatabaseSession,
                                   login_url: str,
                                   valid_email_address: str,
                                   valid_password: str):
    payload = {
        'grant_type': 'password',
        'username': '1',
        'password': valid_password,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = client.post(login_url, data=payload, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_with_wrong_password(client: TestClient,
                                   session: DatabaseSession,
                                   seller: models.User,
                                   login_url: str,
                                   valid_password: str):
    payload = {
        'grant_type': 'password',
        'username': str(seller.user_id),
        'password': valid_password,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = client.post(login_url, data=payload, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
