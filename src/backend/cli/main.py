from backend.cli.database import get_database
from backend.db import models
from backend.security import roles
from backend.settings import load_settings
import datetime
import click


@click.group()
def cli():
    pass


@cli.group('db')
def db():
    pass


@db.command(help="Removes ALL data from database")
def reset():
    database = get_database()
    database.drop_tables()
    database.create_tables()


@db.command(help="Adds dummy seller and admin")
def populate():
    database = get_database()
    with database.session as session:
        session.create_user(models.UserCreate(
            email_address='seller@bct.be',
            role=roles.SELLER.name,
            password='123456789'
        ))
        session.create_user(models.UserCreate(
            email_address='admin@bct.be',
            role=roles.ADMIN.name,
            password='123456789'
        ))
        session.create_sales_event(models.SalesEventCreate(
            date=datetime.date(2030, 12, 18),
            start_time=datetime.time(9, 0),
            end_time=datetime.time(18, 0),
            location='Leuven',
            description='Sales'
        ))
