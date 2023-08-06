import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.db.database import DatabaseSession
from backend.db import models

import datetime


def test_list_events_not_logged_in(client: TestClient,
                                   session: DatabaseSession,
                                   sales_event: models.SalesEventCreate):
    response = client.get('/events')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_events_as_seller(client: TestClient,
                               session: DatabaseSession,
                               seller_access_token: str,
                               sales_event: models.SalesEventCreate):
    headers = {'Authorization': f'Bearer {seller_access_token}'}
    response = client.get('/events', headers=headers)
    json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(json) == 1
    assert len(json[0]) == 6
    assert 'sales_event_id' in json[0]
    assert json[0]['date'] == sales_event.date.isoformat()
    assert json[0]['description'] == sales_event.description
    assert json[0]['start_time'] == sales_event.start_time.isoformat()
    assert json[0]['end_time'] == sales_event.end_time.isoformat()
    assert json[0]['location'] == sales_event.location


def test_list_events_as_admin(client: TestClient,
                              session: DatabaseSession,
                              admin_access_token: str,
                              sales_event: models.SalesEventCreate):
    headers = {'Authorization': f'Bearer {admin_access_token}'}
    response = client.get('/events', headers=headers)
    json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(json) == 1
    assert len(json[0]) == 6
    assert 'sales_event_id' in json[0]
    assert json[0]['date'] == sales_event.date.isoformat()
    assert json[0]['description'] == sales_event.description
    assert json[0]['start_time'] == sales_event.start_time.isoformat()
    assert json[0]['end_time'] == sales_event.end_time.isoformat()
    assert json[0]['location'] == sales_event.location


def test_create_event_as_seller(client: TestClient,
                                session: DatabaseSession,
                                seller_access_token: models.UserCreate):
    payload = {
        'date': datetime.date(2000, 1, 1),
        'start_time': datetime.time(9, 0),
        'end_time': datetime.time(12, 0),
        'location': 'between here and there',
        'description': 'description',
    }
    headers = {'Authorization': f'Bearer {seller_access_token}'}
    response = client.post('/events', data=payload, headers=headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
