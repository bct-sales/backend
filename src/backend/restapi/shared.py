from backend.database.base import Database
from backend.database.memorydb import InMemoryDatabase


def get_database() -> Database:
    global _database
    if _database is None:
        _database = _create_database()
    return _database


def _create_database():
    return InMemoryDatabase()


def set_database(database: Database):
    global _database
    _database = database


_database = None
