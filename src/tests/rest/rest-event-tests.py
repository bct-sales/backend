import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.db.database import DatabaseSession
from backend.db import models

import datetime


def test_list_events_not_logged_in(client: TestClient,
                                   session: DatabaseSession,
                                   sales_event: models.SalesEvent):
    response = client.get('/api/v1/events')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_events_as_seller(client: TestClient,
                               session: DatabaseSession,
                               seller_headers: dict[str, str],
                               sales_event: models.SalesEvent):
    response = client.get('/api/v1/events', headers=seller_headers)
    json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert json == {
        'events': [
            {
                'sales_event_id': sales_event.sales_event_id,
                'date': sales_event.date.isoformat(),
                'description': sales_event.description,
                'start_time': sales_event.start_time.isoformat(),
                'end_time': sales_event.end_time.isoformat(),
                'location': sales_event.location,
                'links': {
                    'edit': f'/events/{sales_event.sales_event_id}'
                }
            },
        ],
        'links': {
            'add': f'/events'
        },
    }


def test_list_events_as_admin(client: TestClient,
                              session: DatabaseSession,
                              admin_headers: dict[str, str],
                              sales_event: models.SalesEvent):
    response = client.get('/api/v1/events', headers=admin_headers)
    json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert json == {
        'events': [
            {
                'sales_event_id': sales_event.sales_event_id,
                'date': sales_event.date.isoformat(),
                'description': sales_event.description,
                'start_time': sales_event.start_time.isoformat(),
                'end_time': sales_event.end_time.isoformat(),
                'location': sales_event.location,
                'links': {
                    'edit': f'/events/{sales_event.sales_event_id}'
                }
            }
        ]
    }


def test_create_event_as_seller(client: TestClient,
                                session: DatabaseSession,
                                seller_headers: dict[str, str]):
    payload = {
        'date': datetime.date(2000, 1, 1).isoformat(),
        'start_time': datetime.time(9, 0).isoformat(),
        'end_time': datetime.time(12, 0).isoformat(),
        'location': 'between here and there',
        'description': 'description',
    }
    response = client.post('/api/v1/events', json=payload, headers=seller_headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize('date', [
    datetime.date(2050, 1, 1),
    datetime.date(2060, 12, 31),
])
@pytest.mark.parametrize('start_time', [
    datetime.time(9, 0),
    datetime.time(10, 30),
])
@pytest.mark.parametrize('end_time', [
    datetime.time(11, 30),
    datetime.time(15, 0),
])
def test_create_event_as_admin(client: TestClient,
                               session: DatabaseSession,
                               admin_headers: dict[str, str],
                               date: datetime.date,
                               start_time: datetime.time,
                               end_time: datetime.time):
    payload = {
        'date': date.isoformat(),
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'location': 'between here and there',
        'description': 'description',
    }
    response = client.post('/api/v1/events', json=payload, headers=admin_headers)

    assert response.status_code == status.HTTP_201_CREATED

    event = models.SalesEvent.model_validate_json(response.read())
    assert event.date == date
    assert event.start_time == start_time
    assert event.end_time == end_time

    events = session.list_sales_events()

    assert len(events) == 1
    event = events[0]
    assert event.date == date
    assert event.start_time == start_time
    assert event.end_time == end_time


def test_edit_event_as_admin(client: TestClient,
                             session: DatabaseSession,
                             admin_headers: dict[str, str],
                             sales_event: models.SalesEvent):
    new_description = 'new description'
    new_location = 'new location'
    payload = {
        'description': new_description,
        'location': new_location
    }
    response = client.put(f'/api/v1/events/{sales_event.sales_event_id}', json=payload, headers=admin_headers)

    assert response.status_code == status.HTTP_200_OK

    orm_sales_event = session.find_sales_event_by_id(sales_event.sales_event_id)
    assert orm_sales_event is not None
    assert orm_sales_event.description == new_description
    assert orm_sales_event.location == new_location
    assert orm_sales_event.date == sales_event.date
    assert orm_sales_event.start_time == sales_event.start_time
    assert orm_sales_event.end_time == sales_event.end_time


def test_edit_event_as_seller(client: TestClient,
                              session: DatabaseSession,
                              seller_headers: dict[str, str],
                              sales_event: models.SalesEvent):
    new_description = 'new description'
    new_location = 'new location'
    payload = {
        'description': new_description,
        'location': new_location
    }
    response = client.put(f'/api/v1/events/{sales_event.sales_event_id}', json=payload, headers=seller_headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
