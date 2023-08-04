import pytest

from backend.database import models
from backend.database.base import DatabaseSession
from backend.database.exceptions import *
from backend.security import roles


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
