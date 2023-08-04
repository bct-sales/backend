import pytest
from backend.security import scopes
from backend.security.tokens import create_access_token, decode_access_token, TokenData
from datetime import timedelta


@pytest.mark.parametrize('email_address', [
    'test@gmail.com',
    'foo@domain.org',
])
@pytest.mark.parametrize('scopes', [
    scopes.Scopes(),
    scopes.Scopes(scopes.LIST_ACCOUNTS),
])
def test_access_token(email_address: str, scopes: scopes.Scopes):
    token_data = TokenData(email_address=email_address, scopes=scopes)
    duration = timedelta(hours=1)
    access_token = create_access_token(token_data=token_data, duration=duration)
    decoded_token_data = decode_access_token(access_token)

    assert decoded_token_data is not None
    assert decoded_token_data.email_address == email_address
    assert decoded_token_data.scopes == scopes
