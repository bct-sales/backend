import os

# Prevents original database_dependency from complaining
os.environ['BCT_DATABASE_PATH'] = ':memory:'

from typing import Iterator

import pydantic
import datetime
import pytest
import logging

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

from backend.app import app
from backend.db.database import Database, DatabaseSession
from backend.db import models, orm
from backend.restapi.shared import database_dependency
from backend.security import roles


test_database = Database(name='Test Database', url='sqlite:///', poolclass=StaticPool)


def database_dependency_override():
    with test_database.session as session:
        yield session


app.dependency_overrides[database_dependency] = database_dependency_override


@pytest.fixture
def valid_email_address():
    return 'test@fake.com'


@pytest.fixture
def invalid_email_address():
    return 'invalid'


@pytest.fixture
def valid_password() -> str:
    return 'ABCDabcd1234!@'


@pytest.fixture
def invalid_password() -> str:
    return 'abcd'


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def database() -> Iterator[Database]:
    logging.info(f"Creating tables in {str(test_database)}")
    test_database.create_tables()
    try:
        yield test_database
    finally:
        logging.info(f"Dropping tables in {str(test_database)}")
        test_database.dispose()


@pytest.fixture
def session(database: Database) -> Iterator[DatabaseSession]:
    session = database.create_session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def seller_password() -> str:
    return 'A B C d 1 23 4 5 +'


@pytest.fixture
def admin_password() -> str:
    return 'x B C d 1 23 4 5 +'


@pytest.fixture
def seller(session: DatabaseSession, seller_password: str) -> orm.User:
    email_address = 'seller@example.com'
    role = roles.SELLER
    user_creation = models.UserCreate(email_address=email_address, role=role.name, password=seller_password)
    return session.create_user(user_creation)


@pytest.fixture
def admin(session: DatabaseSession, admin_password: str) -> orm.User:
    email_address = 'admin@example.com'
    role = roles.ADMIN
    user_creation = models.UserCreate(email_address=email_address, role=role.name, password=admin_password)
    return session.create_user(user_creation)


@pytest.fixture
def seller_access_token(session: DatabaseSession,
                        client: TestClient,
                        seller: orm.User,
                        seller_password: str) -> models.UserCreate:
    payload = {
        'grant_type': 'password',
        'username': seller.email_address,
        'password': seller_password
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = client.post('/login', data=payload, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    access_token = response.json()['access_token']
    return access_token


@pytest.fixture
def admin_access_token(session: DatabaseSession,
                       client: TestClient,
                       admin: orm.User,
                       admin_password: str) -> str:
    payload = {
        'grant_type': 'password',
        'username': admin.email_address,
        'password': admin_password
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = client.post('/login', data=payload, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    access_token = response.json()['access_token']
    return access_token


@pytest.fixture
def sales_event(session: DatabaseSession) -> models.SalesEvent:
    sales_event = models.SalesEventCreate(
        date=datetime.date(2050, 1, 1),
        start_time=datetime.time(9, 0),
        end_time=datetime.time(12, 0),
        location='earth',
        description='only green clothes',
    )
    orm_sales_event = session.create_sales_event(sales_event)
    return models.SalesEvent.model_validate(orm_sales_event)


def create_authorization_headers(token: str):
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def seller_headers(seller_access_token: str) -> dict[str, str]:
    return create_authorization_headers(seller_access_token)


@pytest.fixture
def admin_headers(admin_access_token: str) -> dict[str, str]:
    return create_authorization_headers(admin_access_token)
