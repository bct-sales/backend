import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.db.database import DatabaseSession
from backend.db import models

from tests.util import Exists


def test_list_events_as_cashier(client: TestClient,
                                session: DatabaseSession,
                                cashier_headers: dict[str, str],
                                items: list[models.Item],
                                items_url: str):
    response = client.get(items_url, headers=cashier_headers)
    assert response.status_code == status.HTTP_200_OK
