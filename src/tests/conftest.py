import os

# Prevents original database_dependency from complaining
os.environ['BCT_DATABASE_PATH'] = ':memory:'

from typing import Iterator

import pydantic
import datetime
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

from backend.app import app
from backend.db.database import Database, DatabaseSession
from backend.db import models
from backend.restapi.shared import database_dependency
from backend.security import roles

test_database = Database('sqlite:///', poolclass=StaticPool)


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
    test_database.create_tables()
    try:
        yield test_database
    finally:
        test_database.dispose()


@pytest.fixture
def session(database: Database) -> Iterator[DatabaseSession]:
    session = database.create_session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def seller(session: DatabaseSession) -> models.UserCreate:
    email_address = 'seller@example.com'
    password = 'AJXfksj18392+'
    role = roles.SELLER
    seller = models.UserCreate(email_address=email_address, password=password, role=role.name)
    user_creation = models.UserCreate(email_address=email_address, role=role.name, password=password)
    session.create_user(user_creation)
    return seller


@pytest.fixture
def admin(session: DatabaseSession) -> models.UserCreate:
    email_address = 'admin@example.com'
    password = 'fjkdlAKLDJ19491*'
    role = roles.ADMIN
    seller = models.UserCreate(email_address=email_address, password=password, role=role.name)
    user_creation = models.UserCreate(email_address=email_address, role=role.name, password=password)
    session.create_user(user_creation)
    return seller


@pytest.fixture
def logged_in_seller(session: DatabaseSession, client: TestClient, seller: models.UserCreate) -> models.UserCreate:
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

    return seller


@pytest.fixture
def logged_in_admin(session: DatabaseSession, client: TestClient, admin: models.UserCreate) -> models.UserCreate:
    payload = {
        'grant_type': 'password',
        'username': admin.email_address,
        'password': admin.password
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = client.post('/login', data=payload, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    return admin


@pytest.fixture
def sales_event(session: DatabaseSession) -> models.SalesEventCreate:
    sales_event = models.SalesEventCreate(
        date=datetime.date(2050, 1, 1),
        start_time=datetime.time(9, 0),
        end_time=datetime.time(12, 0),
        location='earth',
        description='only green clothes',
    )
    session.create_sales_event(sales_event)
    return sales_event
