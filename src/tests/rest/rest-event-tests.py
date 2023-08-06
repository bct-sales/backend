import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.db.database import DatabaseSession


# def test_create_event(client: TestClient, session: DatabaseSession, logged_in_seller: User):
#     payload = {

#     }
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }

#     response = client.post('/login', data=payload, headers=headers)

#     assert response.status_code == status.HTTP_200_OK
