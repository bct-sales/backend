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


@router.put('/{item_id}', tags=['items'])
async def update_item(database: DatabaseDependency,
              user: Annotated[orm.User, RequireScopes(scopes.Scopes(
                  scopes.EDIT_OWN_ITEM,
              ))],
              item_id: int,
              update: EditItemData):
    orm_item = database.find_item_by_id(id=item_id)
    if orm_item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if orm_item.owner_id != user.user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    for field, value in update:
        if value is not None:
            setattr(orm_item, field, value)
    database.commit()
