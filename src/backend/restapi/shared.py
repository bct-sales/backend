from backend.database.base import Database


def get_database():
    session = _database.create_session()
    try:
        yield session
    finally:
        session.close()


def _create_database():
    return Database('sqlite:///')


_database = _create_database()
