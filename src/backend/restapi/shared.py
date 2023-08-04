from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi import Depends, HTTPException, status
from backend.database.base import Database
from backend.security import scopes
from backend.security import tokens


def get_database():
    with _database.session as session:
        yield session


def _create_database():
    return Database('sqlite:///')


_database = _create_database()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = 'login',
    scopes = {scope.name: scope.description for scope in scopes.all_scopes()}
)


async def get_current_account(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
    def create_http_exception(message):
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": authenticate_value},
        )

    def has_required_scopes(available_scopes: set[str]):
        expected_scopes = set(security_scopes.scopes)
        return expected_scopes <= available_scopes

    token_data = tokens.decode_access_token(token)
    if not token_data:
        raise create_http_exception('Could not validate credentials')

    if not has_required_scopes(token_data.scopes):
        raise create_http_exception('Not enough permissions')

    try:
        with _database.session as session:
            return session.find_user_with_email_address(email_address=token_data.email_address)
    except:
        # Should never happen
        raise create_http_exception('Unknown user')
