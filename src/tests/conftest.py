import os

# Prevents original database_dependency from complaining
os.environ['BCT_DATABASE_PATH'] = ':memory:'

from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

from backend.app import app
from backend.database.base import Database, DatabaseSession
from backend.restapi.shared import database_dependency

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
