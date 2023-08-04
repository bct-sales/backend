from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer

from backend.database.base import Database, DatabaseSession
from backend.security import scopes, tokens


def database_dependency():
    with _database.session as session:
        yield session


def _create_database():
    return Database('sqlite:///')


DatabaseDependency = Annotated[DatabaseSession, Depends(database_dependency)]


_database = _create_database()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = 'login',
    scopes = {scope.name: scope.description for scope in scopes.all_scopes()}
)


async def get_current_account(required_scopes: scopes.Scopes, token: Annotated[str, Depends(oauth2_scheme)]):
    def create_http_exception(message):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )

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
