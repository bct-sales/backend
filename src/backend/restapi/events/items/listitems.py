from typing import Annotated, Any, Optional

import pydantic
from fastapi import APIRouter, Depends
from backend.db import models

from backend.restapi.shared import *
from backend.security.scopes import Scopes


router = APIRouter()


class _ListItemsResponse_Item_Links(pydantic.BaseModel):
    edit: str


class _ListItemsResponse_Item(models.Item):
    model_config = pydantic.ConfigDict(from_attributes=True)

    links: _ListItemsResponse_Item_Links


class _ListItemsResponse_Links(pydantic.BaseModel):
    add: str

class _ListItemsResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    items: list[_ListItemsResponse_Item]
    links: _ListItemsResponse_Links


@router.get("/",
            response_model=_ListItemsResponse,
            tags=['items'])
async def list_items(event_id: int,
                     database: DatabaseDependency,
                     user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.LIST_OWN_ITEMS))]):
    orm_items = database.list_items_owned_by(owner=user.user_id, sale_event=event_id)
    items = [
        _ListItemsResponse_Item(
            description=item.description,
            item_id=item.item_id,
            owner_id=item.owner_id,
            links=_ListItemsResponse_Item_Links(
                edit=f'/events/{event_id}/items/{item.item_id}',
            ),
            recipient_id=item.recipient_id,
            price_in_cents=item.price_in_cents,
            sales_event_id=item.sales_event_id,
        )
        for item in orm_items
    ]
    return _ListItemsResponse(
        items=items,
        links=_ListItemsResponse_Links(
            add=f'/events/{event_id}/items'
        )
    )
