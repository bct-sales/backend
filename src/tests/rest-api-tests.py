import pytest
from fastapi.testclient import TestClient
from fastapi import status
from backend.app import app
from backend.database.base import Database
from backend.restapi.shared import get_database
from sqlalchemy.pool import StaticPool


test_database = Database('sqlite:///', poolclass=StaticPool)


def get_database_override():
    session = test_database.create_session()
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_database] = get_database_override


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


# def test_get_items(client: TestClient):
#     response = client.get('/items')
#     assert response.status_code == status.HTTP_200_OK
