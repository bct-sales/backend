import pytest

from backend.db import models, orm
from backend.db.database import DatabaseSession
from backend.db.exceptions import *

import datetime


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
def test_create_sales_event(session: DatabaseSession,
                            date: datetime.date,
                            start_time: datetime.time,
                            end_time: datetime.time,
                            location: str,
                            description: str):
    sales_event_create = models.SalesEventCreate(
        date=date,
        start_time=start_time,
        end_time=end_time,
        location=location,
        description=description,
        available=True,
    )
    result = session.create_sales_event(sales_event_create)
    orm_sales_event = session.find_sales_event_by_id(result.sales_event_id)

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
        description="it's red",
        available=True,
    )
    with pytest.raises(InvalidEventTimeInterval):
        session.create_sales_event(sales_event)
