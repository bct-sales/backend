import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.database import models
from backend.database.base import DatabaseSession
from backend.security import roles


def test_register(client: TestClient, session: DatabaseSession, valid_email_address: str, valid_password: str):
    payload = {
        'email_address': valid_email_address,
        'password': valid_password
    }
    response = client.post('/register', json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert len(session.list_users()) == 1


def test_register_with_existing_email_address(client: TestClient, session: DatabaseSession, valid_email_address: str, valid_password: str):
    user_creation_data = models.UserCreate(
        email_address=valid_email_address,
        password=valid_password,
        role=roles.SELLER.name,
    )
    session.create_user(user_creation_data)
    assert len(session.list_users()) == 1

    payload = {
        'email_address': valid_email_address,
        'password': valid_password
    }
    response = client.post('/register', json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(session.list_users()) == 1


def test_register_with_invalid_email_address(client: TestClient, session: DatabaseSession, invalid_email_address: str, valid_password: str):
    payload = {
        'email_address': invalid_email_address,
        'password': valid_password
    }
    response = client.post('/register', json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(session.list_users()) == 0


def test_register_with_invalid_password(client: TestClient, session: DatabaseSession, valid_email_address: str, invalid_password: str):
    payload = {
        'email_address': valid_email_address,
        'password': invalid_password
    }
    response = client.post('/register', json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(session.list_users()) == 0
