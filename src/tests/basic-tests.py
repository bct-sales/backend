from backend.security.password import is_valid_password
from backend.security.validation import is_valid_email_address


def test_valid_email_address(valid_email_address: str):
    assert is_valid_email_address(valid_email_address)


def test_invalid_email_address(invalid_email_address: str):
    assert not is_valid_email_address(invalid_email_address)


def test_valid_password(valid_password: str):
    assert is_valid_password(valid_password)


def test_invalid_password(invalid_password: str):
    assert not is_valid_password(invalid_password)
