from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from backend.db import orm
from backend.db.base import Database, DatabaseSession
from backend.security import scopes, tokens
from backend.security.roles import Role
from backend.settings import load_settings

import logging
import sys
import os


def database_dependency():
    global _database
    if not _database:
        _database = _create_database()

    with _database.session as session:
        yield session


def _create_database():
    settings = load_settings()

    if settings.database_path is None:
        logging.error("Use BCT_DATABASE_PATH to specify which database to use")
        sys.exit(-1)

    if settings.database_path != ':memory:' and not os.path.isfile(settings.database_path):
        logging.error("Database does not exist")
        sys.exit(-2)

    settings = load_settings()
    return Database(settings.database_url)


DatabaseDependency = Annotated[DatabaseSession, Depends(database_dependency)]


_database = _create_database()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = 'login',
    scopes = {scope.name: scope.description for scope in scopes.all_scopes()}
)

def get_current_user(required_scopes: scopes.Scopes, access_token: str) -> orm.User:
    access_token_data = tokens.decode_access_token(access_token)

    if not access_token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid access token',
            headers={"WWW-Authenticate": "Bearer"}
        )

    available_scopes = access_token_data.scopes
    if not available_scopes.has_permissions_for(required_scopes):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No permission',
            headers={"WWW-Authenticate": "Bearer"}
        )

    with _database.session as session:
        user = session.find_user_with_email_address(email_address=access_token_data.email_address)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Unknown user',
                headers={"WWW-Authenticate": "Bearer"}
            )
        return user


def RequireScopes(required_scopes: scopes.Scopes) -> orm.User:
    def dependency(token: Annotated[str, Depends(oauth2_scheme)]):
        return get_current_user(required_scopes, token)

    return Depends(dependency)