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
                     user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.LIST_OWN_ITEMS))]):
    return database.list_items_owned_by(user.user_id)


@router.post("/items", response_model=models.Item, status_code=status.HTTP_201_CREATED)
async def create_item(database: DatabaseDependency,
                      user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.ADD_ITEM))],
                      item: models.ItemCreate):
    orm_item = database.create_item(item=item, owner_id=user.user_id)
    return models.Item.model_validate(orm_item)
