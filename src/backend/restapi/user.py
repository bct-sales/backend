from typing import Annotated, Any

import pydantic
from fastapi import APIRouter, Depends
from backend.db import models

from backend.restapi.shared import *
from backend.security.scopes import Scopes


router = APIRouter(
    tags=['items']
)


@router.get("/items", response_model=list[models.Item])
async def list_items(database: DatabaseDependency,
                     user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.ADD_ITEM))]):
    return database.list_items_owned_by(user.user_id)
