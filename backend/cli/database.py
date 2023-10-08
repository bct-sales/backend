import datetime
import io
import logging
import sys
from pathlib import Path

import click

from backend.db import models, orm
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
    item_categories = [
        'Clothing 0-3 mos (50-56)',
        'Clothing 3-6 mos (56-62)',
        'Clothing 6-12 mos (68-80)',
        'Clothing 12-24 mos (86-92)',
        'Clothing 2-3 yrs (92-98)',
        'Clothing 4-6 yrs (104-116)',
        'Clothing 7-8 yrs (122-134)',
        'Toys',
        'Baby/Child Equipment',
        'Large Items',
    ]
    database = get_database()
    database.drop_tables()
    database.create_tables()
    with database.session as session:
        session.create_user_with_id(
            1,
            models.UserCreate(
                role=roles.ADMIN.name,
                password='111'
            )
        )
        seller = session.create_user_with_id(
            2,
            models.UserCreate(
                role=roles.SELLER.name,
                password='222'
            )
        )
        session.create_user_with_id(
            3,
            models.UserCreate(
                role=roles.CASHIER.name,
                password='333'
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
            category=item_categories[0],
            charity=False,
            price_in_cents=200,
            recipient_id=seller.user_id,
            sales_event_id=event.sales_event_id,
            owner_id=seller.user_id))
        session.create_item(item=models.ItemCreate(
            description='Black shirt',
            category=item_categories[0],
            charity=True,
            price_in_cents=800,
            recipient_id=seller.user_id,
            sales_event_id=event.sales_event_id,
            owner_id=seller.user_id))
        session.create_item(item=models.ItemCreate(
            description='Red pants',
            category=item_categories[3],
            charity=True,
            price_in_cents=5000,
            recipient_id=seller.user_id,
            sales_event_id=event.sales_event_id,
            owner_id=seller.user_id))
        session.create_item(item=models.ItemCreate(
            description='Blue Jeans',
            category=item_categories[4],
            charity=True,
            price_in_cents=2000,
            recipient_id=seller.user_id,
            sales_event_id=event.sales_event_id,
            owner_id=seller.user_id))


@db.group(name="import", help='Imports data from csv file')
def _import():
    # this is a group, so no implementation necessary
    pass


@_import.command(name='sellers', help='Imports sellers from csv file')
@click.argument('file', type=click.File(mode='r', encoding='utf-8'))
def users(file: io.TextIOWrapper) -> None:
    import csv
    database = get_database()
    reader = csv.reader(file)
    for row in reader:
        if len(row) != 2:
            print("Each row should contain two values: id,password")
            sys.exit(-1)
        id_string, password = row
        id = int(id_string)
        with database.session as session:
            data = models.UserCreate(
                role='seller',
                password=password,
            )
            session.create_user_with_id(id, data)
            print(f"Created seller {id}")


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


@db.command(name='add-user')
@click.option('--role', type=click.Choice(['admin', 'seller', 'cashier']))
@click.option('--id', type=int)
@click.option('--password', type=str)
def add_user(role: roles.RoleName, id: int, password: str) -> int:
    """
    Creates new user
    """
    database = get_database()
    with database.session as session:
        if session.find_user_with_id(user_id = id) is not None:
            print(f"Already a user with id {id}")
            return -1
        user_data = models.UserCreate(
            role=role,
            password=password
        )
        session.create_user_with_id(user_id=id, user=user_data)
        print("User successfully created")
        return 0


@db.command(name='list-users')
def list_users() -> None:
    """
    Lists all users as csv
    """
    import csv
    database = get_database()
    with database.session as session:
        users: list[orm.User] = session.list_users()
        csv_writer = csv.DictWriter(
            sys.stdout,
            fieldnames=['user_id', 'role']
        )
        csv_writer.writeheader()
        for user in users:
            csv_writer.writerow({
                'user_id': user.user_id,
                'role': user.role,
            })


@db.command(name="list-items")
def list_items() -> None:
    """
    Lists all items as csv
    """
    import csv
    database = get_database()
    with database.session as session:
        items: list[orm.Item] = session.list_items()
        csv_writer = csv.DictWriter(
            sys.stdout,
            fieldnames=['item_id', 'description', 'category', 'price_in_cents', 'owner_id', 'recipient_id', 'sales_event_id', 'charity']
        )
        csv_writer.writeheader()
        for item in items:
            csv_writer.writerow({
                'item_id': item.item_id,
                'description': item.description,
                'category': item.category,
                'price_in_cents': item.price_in_cents,
                'owner_id': item.owner_id,
                'recipient_id': item.recipient_id,
                'sales_event_id': item.sales_event_id,
                'charity': int(item.charity)
            })
