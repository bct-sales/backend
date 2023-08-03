import pytest
from backend.database.base import Database, DatabaseSession
from backend.database import models
from sqlalchemy.pool import StaticPool


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


def test_create_user(session: DatabaseSession):
    # Arrange
    email_address = 'test@gmail.com'
    password = 'xyz'
    user = models.UserCreate(email_address=email_address, password=password)
    session.create_user(user)
    session.commit()

    # Act
    actual = session.login(email_address=email_address, password=password)

    # Assert
    assert actual is not None
    assert actual.email_address == email_address

