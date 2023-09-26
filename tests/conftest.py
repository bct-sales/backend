import os

# Prevents original database_dependency from complaining
os.environ['BCT_DATABASE_PATH'] = ':memory:'

from typing import Callable, Iterator

import pydantic
import datetime
import pytest
import logging

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

from backend.app import app
from backend.db.database import Database, DatabaseSession
from backend.db import models, orm
from backend.restapi.shared import database_dependency
from backend.security import roles

import backend.restapi.events
import backend.restapi.events.items


test_database = Database(name='Test Database', url='sqlite:///', poolclass=StaticPool)


def database_dependency_override():
    with test_database.session as session:
        yield session


app.dependency_overrides[database_dependency] = database_dependency_override


@pytest.fixture
def valid_password() -> str:
    return 'ABCDabcd1234!@'


@pytest.fixture
def invalid_password() -> str:
    return 'a'


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def database() -> Iterator[Database]:
    logging.info(f"Creating tables in {str(test_database)}")
    test_database.create_tables()
    try:
        yield test_database
    finally:
        logging.info(f"Dropping tables in {str(test_database)}")
        test_database.dispose()


@pytest.fixture
def session(database: Database) -> Iterator[DatabaseSession]:
    session = database.create_session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def seller_password() -> str:
    return 'A B C d 1 23 4 5 +'


@pytest.fixture
def admin_password() -> str:
    return 'x B C d 1 23 4 5 +'


@pytest.fixture
def seller(session: DatabaseSession, seller_password: str) -> models.User:
    role = roles.SELLER
    user_creation = models.UserCreate(role=role.name, password=seller_password)
    orm_user = session.create_user_with_id(2, user_creation)
    return models.User.model_validate(orm_user)


@pytest.fixture
def admin(session: DatabaseSession, admin_password: str) -> models.User:
    role = roles.ADMIN
    user_creation = models.UserCreate(role=role.name, password=admin_password)
    orm_user = session.create_user_with_id(1, user_creation)
    return models.User.model_validate(orm_user)


@pytest.fixture
def seller_access_token(session: DatabaseSession,
                        client: TestClient,
                        seller: models.User,
                        login_url: str,
                        seller_password: str) -> models.UserCreate:
    payload = {
        'grant_type': 'password',
        'username': seller.user_id,
        'password': seller_password
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = client.post(login_url, data=payload, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    access_token = response.json()['access_token']
    return access_token


@pytest.fixture
def admin_access_token(session: DatabaseSession,
                       client: TestClient,
                       admin: orm.User,
                       login_url: str,
                       admin_password: str) -> str:
    payload = {
        'grant_type': 'password',
        'username': admin.user_id,
        'password': admin_password
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = client.post(login_url, data=payload, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    access_token = response.json()['access_token']
    return access_token


@pytest.fixture
def sales_event(session: DatabaseSession) -> models.SalesEvent:
    sales_event = models.SalesEventCreate(
        date=datetime.date(2050, 1, 1),
        start_time=datetime.time(9, 0),
        end_time=datetime.time(12, 0),
        location='earth',
        description='only green clothes',
        available=True,
    )
    orm_sales_event = session.create_sales_event(sales_event)
    return models.SalesEvent.model_validate(orm_sales_event)


@pytest.fixture
def unavailable_sales_event(session: DatabaseSession) -> models.SalesEvent:
    sales_event = models.SalesEventCreate(
        date=datetime.date(2060, 1, 1),
        start_time=datetime.time(9, 0),
        end_time=datetime.time(12, 0),
        location='mars',
        description='only red clothes',
        available=False,
    )
    orm_sales_event = session.create_sales_event(sales_event)
    return models.SalesEvent.model_validate(orm_sales_event)


@pytest.fixture
def item(session: DatabaseSession, sales_event: models.SalesEvent, seller: models.User) -> models.Item:
    item = models.ItemCreate(
        description='Sneakers',
        price_in_cents=1000,
        recipient_id=seller.user_id,
        sales_event_id=sales_event.sales_event_id,
        owner_id=seller.user_id,
        charity=False,
    )
    orm_item = session.create_item(item=item)
    return models.Item.model_validate(orm_item)


def create_authorization_headers(token: str):
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def seller_headers(seller_access_token: str) -> dict[str, str]:
    return create_authorization_headers(seller_access_token)


@pytest.fixture
def admin_headers(admin_access_token: str) -> dict[str, str]:
    return create_authorization_headers(admin_access_token)



class ApiRootLinks(pydantic.BaseModel):
    login: str
    events: str

class ApiRootData(pydantic.BaseModel):
    links: ApiRootLinks


@pytest.fixture
def api_root(client: TestClient):
    response = client.get('/api/v1')
    assert response.status_code == status.HTTP_200_OK
    return ApiRootData.model_validate(response.json())


@pytest.fixture
def login_url(api_root: ApiRootData):
    return api_root.links.login


@pytest.fixture
def events_url(api_root: ApiRootData):
    return api_root.links.events



FetchEvents = Callable[[dict[str, str]], backend.restapi.events.listevents.Response]

@pytest.fixture
def fetch_events(client: TestClient,
                 events_url: str) -> FetchEvents:
    def fetch(headers: dict[str, str]):
        response = client.get(events_url, headers=headers)
        return backend.restapi.events.listevents.Response.model_validate(response.json())
    return fetch


FetchEvent = Callable[[dict[str, str], int], backend.restapi.events.listevents.Event]

@pytest.fixture
def fetch_event(fetch_events: FetchEvents) -> FetchEvent:
    def fetch(headers: dict[str, str], event_id: int):
        events = fetch_events(headers).events
        return next(event
                    for event in events
                    if event.sales_event_id == event_id)
    return fetch


FetchItem = Callable[[dict[str, str], int, int], backend.restapi.events.items.listitems.Item]

@pytest.fixture
def fetch_item(client: TestClient,
               fetch_event: FetchEvent) -> FetchItem:
    def fetch(headers: dict[str, str], event_id: int, item_id: int):
        items_url = fetch_event(headers, event_id).links.items
        response = client.get(items_url, headers=headers)
        item = next(item for item in response.json()['items'] if item['item_id'] == item_id)
        return backend.restapi.events.items.listitems.Item.model_validate(item)

    return fetch
