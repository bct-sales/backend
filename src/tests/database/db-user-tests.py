import sqlalchemy.exc
import pytest

from backend.db import models
from backend.db.database import DatabaseSession
from backend.db.exceptions import *
from backend.security import roles


@pytest.mark.parametrize("user_id", [
    1,
    5,
    100,
    491,
])
def test_create_user(session: DatabaseSession, valid_password: str, user_id: int):
    user = models.UserCreate(password=valid_password, role=roles.SELLER.name)
    session.create_user_with_id(user_id, user)

    actual = session.login_with_id(user_id=user_id, password=valid_password)

    assert actual is not None
    assert actual.user_id == user_id


@pytest.mark.parametrize("user_id", [
    1,
    5,
    100,
    491,
])
def test_create_user_with_existing_id(session: DatabaseSession, valid_password: str, user_id: int):
    user = models.UserCreate(password=valid_password, role=roles.SELLER.name)
    session.create_user_with_id(user_id, user)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        session.create_user_with_id(user_id, user)
