from typing import Annotated, Any

import pydantic
from fastapi import APIRouter, Depends
from backend.db import models

from backend.restapi.shared import *
from backend.security.scopes import Scopes


router = APIRouter(
    tags=['items']
)


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


@router.get("/events/{event_id}/items", response_model=_ListItemsResponse)
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
                edit=f'/api/v1/items/{item.item_id}',
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
            add='/api/v1/me/events/{event_id}/items'
        )
    )


@router.post("/items", response_model=models.Item, status_code=status.HTTP_201_CREATED)
async def create_item(database: DatabaseDependency,
                      user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.ADD_ITEM))],
                      item: models.ItemCreate):
    orm_item = database.create_item(item=item, owner_id=user.user_id)
    return models.Item.model_validate(orm_item)
