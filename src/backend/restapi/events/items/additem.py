from typing import Annotated, Any, Optional

import pydantic
from fastapi import APIRouter, Depends
from backend.db import models

from backend.restapi.shared import *
from backend.security.scopes import Scopes


router = APIRouter()


class _CreateItemPayload(pydantic.BaseModel):
    description: str
    price_in_cents: pydantic.NonNegativeInt
    recipient_id: int


@router.post("/",
             response_model=models.Item,
             status_code=status.HTTP_201_CREATED,
             tags=['items'])
async def create_item(database: DatabaseDependency,
                      user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.ADD_OWN_ITEM))],
                      event_id: int,
                      payload: _CreateItemPayload):
    item = models.ItemCreate(
        **dict(payload),
        sales_event_id=event_id,
        owner_id=user.user_id
    )
    orm_item = database.create_item(item=item)
    return models.Item.model_validate(orm_item)
