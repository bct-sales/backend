import pytest
from backend.database.base import Database, DatabaseSession
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


def test_list_users(session: DatabaseSession):
    users = session.list_users()
    assert len(users) == 0
