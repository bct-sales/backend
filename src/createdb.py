from backend.db import models
from backend.db.database import Database
from backend.security import roles
from backend.settings import load_settings
import logging
import sys
import os


settings = load_settings()

if (database_path := settings.database_path) is None:
    logging.error('No database path set; use BCT_DATABASE_PATH environment variable')
    sys.exit(-1)

if os.path.isfile(database_path):
    logging.error('Database already exists')
    sys.exit(-2)

database = Database(name="Production Database", url=settings.database_url)

database.create_tables()

with database.session as session:
    session.create_user(models.UserCreate(email_address='seller@bct.be', role=roles.SELLER.name, password='123456789'))
    session.create_user(models.UserCreate(email_address='admin@bct.be', role=roles.ADMIN.name, password='123456789'))
