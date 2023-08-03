import pytest
from fastapi.testclient import TestClient
from fastapi import status
from backend.app import app
from backend.database.memorydb import InMemoryDatabase
from backend.restapi.shared import set_database


def reset_database():
    set_database(InMemoryDatabase())


@pytest.fixture
def client():
    reset_database()
    with TestClient(app) as client:
        yield client


def test_get_items(client: TestClient):
    response = client.get('/items')
    assert response.status_code == status.HTTP_200_OK
