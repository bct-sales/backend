from typing import Annotated, Any, Optional

import pydantic
from fastapi import APIRouter, Depends

from backend.db import models
from backend.restapi.shared import *
from backend.security.scopes import Scopes

router = APIRouter()


class EditItemData(pydantic.BaseModel):
    description: Optional[str] = None
    price_in_cents: Optional[int] = None
    recipient_id: Optional[int] = None
    sales_event_id: Optional[int] = None
    charity: Optional[bool] = None


@router.put('/{item_id}', tags=['items'])
async def update_item(database: DatabaseDependency,
                      user: Annotated[orm.User, RequireScopes(scopes.Scopes(
                          scopes.EDIT_OWN_ITEM,
                      ))],
                      item_id: int,
                      update: EditItemData):
    database.update_item(item_id=item_id, owner_id=user.user_id, **dict(update))
