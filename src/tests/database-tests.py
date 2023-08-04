import pytest
from backend.database.base import Database, DatabaseSession
from backend.database import models
from sqlalchemy.pool import StaticPool

from backend.database.exceptions import *


@pytest.fixture
def database():
    database = Database('sqlite:///', poolclass=StaticPool)
    database.create_tables()
    try:
        yield database
    finally:
        database.dispose()


@pytest.fixture
def session(database: Database):
    session = database.create_session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def valid_password() -> str:
    return 'ABCDabcd1234!@'


def test_create_user(session: DatabaseSession, valid_password: str):
    email_address = 'test@gmail.com'
    user = models.UserCreate(email_address=email_address, password=valid_password)
    session.create_user(user)

    actual = session.login(email_address=email_address, password=valid_password)

    assert actual is not None
    assert actual.email_address == email_address


def test_create_user_with_existing_email_address(session: DatabaseSession, valid_password: str):
    email_address = 'test@gmail.com'
    user = models.UserCreate(email_address=email_address, password=valid_password)
    session.create_user(user)

    with pytest.raises(EmailAddressAlreadyInUseException):
        session.create_user(user)
