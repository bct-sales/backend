import datetime
import logging
import sys

import click

from backend.db import models
from backend.db.database import Database
from backend.security import roles
from backend.settings import load_settings


def get_database() -> Database:
    settings = load_settings()

    if settings.database_path is None:
        logging.error('No database path set; use BCT_DATABASE_PATH environment variable')
        sys.exit(-1)

    return Database(name="Production Database", url=settings.database_url)


@click.group('db')
def db():
    pass


@db.command(help="Removes ALL data from database")
def reset():
    database = get_database()
    database.drop_tables()
    database.create_tables()


@db.command(help="Removes ALL data and adds dummy seller and admin")
def repopulate():
    database = get_database()
    database.drop_tables()
    database.create_tables()
    with database.session as session:
        session.create_user(models.UserCreate(
            email_address='admin@bct.be',
            role=roles.ADMIN.name,
            password='123456789'
        ))
        seller = session.create_user(models.UserCreate(
            email_address='seller@bct.be',
            role=roles.SELLER.name,
            password='123456789'
        ))
        event = session.create_sales_event(models.SalesEventCreate(
            date=datetime.date(2023, 12, 18),
            start_time=datetime.time(9, 0),
            end_time=datetime.time(18, 0),
            location='Leuven',
            description='Leuven Sales',
            available=True,
        ))
        session.create_sales_event(models.SalesEventCreate(
            date=datetime.date(2040, 1, 1),
            start_time=datetime.time(10, 0),
            end_time=datetime.time(12, 0),
            location='Brussels',
            description='Brussels Sales',
            available=True,
        ))
        session.create_sales_event(models.SalesEventCreate(
            date=datetime.date(2050, 1, 1),
            start_time=datetime.time(10, 0),
            end_time=datetime.time(12, 0),
            location='Antwerp',
            description='Antwerp Sales',
            available=True,
        ))
        session.create_sales_event(models.SalesEventCreate(
            date=datetime.date(2060, 1, 1),
            start_time=datetime.time(10, 0),
            end_time=datetime.time(12, 0),
            location='Ghent',
            description='Ghent Sales',
            available=True,
        ))
        session.create_item(item=models.ItemCreate(
            description='T-Shirt',
            charity=False,
            price_in_cents=200,
            recipient_id=seller.user_id,
            sales_event_id=event.sales_event_id,
            owner_id=seller.user_id))
        session.create_item(item=models.ItemCreate(
            description='Jeans',
            charity=True,
            price_in_cents=800,
            recipient_id=seller.user_id,
            sales_event_id=event.sales_event_id,
            owner_id=seller.user_id))
