from backend.database.base import Database
from backend.settings import load_settings
import logging
import sys
import os


settings = load_settings()

if os.path.isfile(settings.database_path):
    logging.error('Database already exists')
    sys.exit(-1)

database = Database(url=settings.database_url)

database.create_tables()
