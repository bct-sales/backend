from backend.security.password import is_valid_password


def test_seller_password_valid_password(seller_password: str, valid_password: str):
    assert seller_password != valid_password, 'Bug in tests: seller.password should not be equal to valid password'


def test_valid_password(valid_password: str):
    assert is_valid_password(valid_password)


def test_invalid_password(invalid_password: str):
    assert not is_valid_password(invalid_password)
