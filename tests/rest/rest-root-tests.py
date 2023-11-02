import pytest
from fastapi import status
from fastapi.testclient import TestClient

from tests.util import Exists


def test_root(client: TestClient):
    response = client.get('/api/v1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'links': {
            'login': Exists(),
            'events': Exists(),
            'items': Exists(),
            'sales': Exists(),
        }
    }
