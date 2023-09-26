import pytest
from backend.security import scopes
from backend.security.tokens import create_access_token, decode_access_token, TokenData
from datetime import timedelta


@pytest.mark.parametrize('user_id', [
    1,
    15,
    951
])
@pytest.mark.parametrize('scopes', [
    scopes.Scopes(),
    scopes.Scopes(scopes.LIST_ACCOUNTS),
])
def test_access_token(user_id: int, scopes: scopes.Scopes):
    token_data = TokenData(user_id=user_id, scopes=scopes)
    duration = timedelta(hours=1)
    access_token = create_access_token(token_data=token_data, duration=duration)
    decoded_token_data = decode_access_token(access_token)

    assert decoded_token_data is not None
    assert decoded_token_data.user_id == user_id
    assert decoded_token_data.scopes == scopes
