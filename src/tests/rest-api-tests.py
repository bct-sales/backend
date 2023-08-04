import pytest
from fastapi.testclient import TestClient
from fastapi import status
from backend.app import app
from backend.database import models
from backend.database.base import Database, DatabaseSession
from backend.restapi.shared import database_dependency
from sqlalchemy.pool import StaticPool
from backend.security import roles


test_database = Database('sqlite:///', poolclass=StaticPool)


def database_dependency_override():
    with test_database.session as session:
        yield session


app.dependency_overrides[database_dependency] = database_dependency_override


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def valid_email_address():
    return 'test@fake.com'


@pytest.fixture
def valid_password() -> str:
    return 'ABCDabcd1234!@'


@pytest.fixture
def database():
    test_database.create_tables()
    yield test_database
    test_database.dispose()


@pytest.fixture
def session(database: Database):
    with database.session as session:
        yield session


def test_get_items(client: TestClient):
    response = client.get('/items')
    assert response.status_code == status.HTTP_200_OK


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