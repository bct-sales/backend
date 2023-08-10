from backend.cli.database import get_database
from backend.db import models
from backend.security import roles
from backend.security.tokens import create_access_token, TokenData
import datetime
import click
import sys


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


@db.command(help="Removes ALL data and adds dummy seller and admin")
def repopulate():
    database = get_database()
    database.drop_tables()
    database.create_tables()
    with database.session as session:
        seller = session.create_user(models.UserCreate(
            email_address='seller@bct.be',
            role=roles.SELLER.name,
            password='123456789'
        ))
        session.create_user(models.UserCreate(
            email_address='admin@bct.be',
            role=roles.ADMIN.name,
            password='123456789'
        ))
        event = session.create_sales_event(models.SalesEventCreate(
            date=datetime.date(2030, 12, 18),
            start_time=datetime.time(9, 0),
            end_time=datetime.time(18, 0),
            location='Leuven',
            description='Leuven Sales'
        ))
        session.create_sales_event(models.SalesEventCreate(
            date=datetime.date(2040, 1, 1),
            start_time=datetime.time(10, 0),
            end_time=datetime.time(12, 0),
            location='Brussels',
            description='Brussels Sales'
        ))
        session.create_sales_event(models.SalesEventCreate(
            date=datetime.date(2050, 1, 1),
            start_time=datetime.time(10, 0),
            end_time=datetime.time(12, 0),
            location='Antwerp',
            description='Antwerp Sales'
        ))
        session.create_sales_event(models.SalesEventCreate(
            date=datetime.date(2060, 1, 1),
            start_time=datetime.time(10, 0),
            end_time=datetime.time(12, 0),
            location='Ghent',
            description='Ghent Sales'
        ))
        session.create_item(item=models.ItemCreate(
            description='T-Shirt',
            price_in_cents=200,
            recipient_id=seller.user_id,
            sales_event_id=event.sales_event_id
        ), owner_id=seller.user_id)
        session.create_item(item=models.ItemCreate(
            description='Jeans',
            price_in_cents=800,
            recipient_id=seller.user_id,
            sales_event_id=event.sales_event_id
        ), owner_id=seller.user_id)


@cli.group
def token():
    pass


@token.command
@click.argument('user')
def create(user):
    database = get_database()
    with database.session as session:
        user = session.find_user_with_email_address(email_address=user)

    if user is None:
        print(f'Error: no user found with email address {user}')
        sys.exit(-1)

    role = roles.Role.from_name(user.role)
    token_data = TokenData(user_id=user.user_id, scopes=role.scopes)
    access_token = create_access_token(token_data=token_data, duration=datetime.timedelta(days=365))
    print(access_token)
