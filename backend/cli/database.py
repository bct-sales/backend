import datetime
import io
import logging
import sys
from pathlib import Path

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
def testdata():
    database = get_database()
    database.drop_tables()
    database.create_tables()
    with database.session as session:
        session.create_user_with_id(
            1,
            models.UserCreate(
                role=roles.ADMIN.name,
                password='123456789'
            )
        )
        seller = session.create_user_with_id(
            2,
            models.UserCreate(
                role=roles.SELLER.name,
                password='123456789'
            )
        )
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
            description='Blue shirt',
            charity=False,
            price_in_cents=200,
            recipient_id=seller.user_id,
            sales_event_id=event.sales_event_id,
            owner_id=seller.user_id))
        session.create_item(item=models.ItemCreate(
            description='Black shirt',
            charity=True,
            price_in_cents=800,
            recipient_id=seller.user_id,
            sales_event_id=event.sales_event_id,
            owner_id=seller.user_id))
        session.create_item(item=models.ItemCreate(
            description='Red pants',
            charity=True,
            price_in_cents=5000,
            recipient_id=seller.user_id,
            sales_event_id=event.sales_event_id,
            owner_id=seller.user_id))


@db.group(name="import", help='Imports data from csv file')
def _import():
    pass


@_import.command(name='users', help='Imports users from csv file')
@click.argument('file', type=click.File(mode='r', encoding='utf-8'))
def users(file: io.TextIOWrapper) -> None:
    import csv
    database = get_database()
    reader = csv.reader(file)
    for row in reader:
        if len(row) != 2:
            print("Each row should contain two values: id,password")
            sys.exit(-1)
        id, password = row
        id = int(id)
        with database.session as session:
            data = models.UserCreate(
                role='seller',
                password=password,
            )
            session.create_user_with_id(id, data)


@db.command(help='Imports users from csv file')
def backup() -> None:
    def progress(status: int, remaining: int, total: int):
        print(f'{remaining} remaining')

    import sqlite3
    cfg = load_settings()
    database_path = load_settings().database_path
    backup_filename = datetime.datetime.today().strftime("backup-%Y%m%d-%H%M%S.db")
    backup_directory = Path(cfg.db_backup_directory)
    backup_path = backup_directory / backup_filename

    src = sqlite3.connect(str(database_path))
    dst = sqlite3.connect(backup_path)
    with dst:
        src.backup(dst, progress=progress)
    dst.close()
    src.close()
