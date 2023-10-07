from typing import Annotated

import pydantic
from fastapi import APIRouter, Depends

from backend.db import models
from backend.restapi.shared import *

router = APIRouter()


class AddItemData(pydantic.BaseModel):
    description: str
    category: str
    price_in_cents: pydantic.NonNegativeInt
    recipient_id: int
    charity: bool


@router.post("/",
             response_model=models.Item,
             status_code=status.HTTP_201_CREATED,
             tags=['items'])
async def add_item(database: DatabaseDependency,
                   user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.ADD_OWN_ITEM))],
                   event_id: int,
                   payload: AddItemData):
    item = models.ItemCreate(
        description=payload.description,
        category=payload.category,
        price_in_cents=payload.price_in_cents,
        recipient_id=payload.recipient_id,
        charity=payload.charity,
        sales_event_id=event_id,
        owner_id=user.user_id
    )
    orm_item = database.create_item(item=item)
    return models.Item.model_validate(orm_item)
