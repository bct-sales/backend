from backend.db.database import Database
from backend.settings import load_settings
import logging
import sys


def get_database() -> Database:
    settings = load_settings()

    if settings.database_path is None:
        logging.error('No database path set; use BCT_DATABASE_PATH environment variable')
        sys.exit(-1)

    return Database(name="Production Database", url=settings.database_url)
