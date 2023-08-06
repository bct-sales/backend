import pytest

from backend.database import models
from backend.database.base import DatabaseSession
from backend.database.exceptions import *
from backend.security import roles

import datetime


def test_create_user(session: DatabaseSession, valid_password: str):
    email_address = 'test@gmail.com'
    user = models.UserCreate(email_address=email_address, password=valid_password, role=roles.SELLER.name)
    session.create_user(user)

    actual = session.login(email_address=email_address, password=valid_password)

    assert actual is not None
    assert actual.email_address == email_address


def test_create_user_with_existing_email_address(session: DatabaseSession, valid_email_address: str, valid_password: str):
    user = models.UserCreate(email_address=valid_email_address, password=valid_password, role=roles.SELLER.name)
    session.create_user(user)
    with pytest.raises(EmailAddressAlreadyInUseException):
        session.create_user(user)


def test_create_user_with_invalid_email_address(session: DatabaseSession, invalid_email_address: str, valid_password: str):
    user = models.UserCreate(email_address=invalid_email_address, password=valid_password, role=roles.SELLER.name)

    with pytest.raises(InvalidEmailAddressException):
        session.create_user(user)


@pytest.mark.parametrize('date', [
    datetime.date(year, month, day)
    for year in [2000, 2010]
    for month in [1, 5, 9, 12]
    for day in [1, 5, 28]
])
@pytest.mark.parametrize('start_time', [
    datetime.time(hour=9, minute=0),
    datetime.time(hour=10, minute=30),
])
@pytest.mark.parametrize('end_time', [
    datetime.time(hour=11, minute=0),
    datetime.time(hour=15, minute=30),
])
@pytest.mark.parametrize('location', [
    'Brussels',
    'Antwerp'
])
@pytest.mark.parametrize('description', [
    '',
    'some description'
])
def test_create_sales_event(session: DatabaseSession, date: datetime.date, start_time: datetime.time, end_time: datetime.time, location: str, description: str):
    sales_event = models.SalesEventCreate(
        date=date,
        start_time=start_time,
        end_time=end_time,
        location=location,
        description=description
    )
    event_id = session.create_sales_event(sales_event)
    orm_sales_event = session.find_sales_event_by_id(event_id)

    assert orm_sales_event is not None
    assert orm_sales_event.date == date
    assert orm_sales_event.start_time == start_time
    assert orm_sales_event.end_time == end_time
    assert orm_sales_event.location == location
    assert orm_sales_event.description == description


def test_create_sales_event_with_invalid_time(session: DatabaseSession):
    sales_event = models.SalesEventCreate(
        date=datetime.date(2000, 1, 1),
        start_time=datetime.time(19, 0),
        end_time=datetime.time(9, 0),
        location='here',
        description="it's red"
    )
    with pytest.raises(InvalidEventTimeInterval):
        session.create_sales_event(sales_event)