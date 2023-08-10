from typing import Annotated, Any, Optional

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
                edit=f'/api/v1/me/items/{item.item_id}',
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
            add=f'/api/v1/me/events/{event_id}/items'
        )
    )


@router.post("/items", response_model=models.Item, status_code=status.HTTP_201_CREATED)
async def create_item(database: DatabaseDependency,
                      user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.ADD_OWN_ITEM))],
                      item: models.ItemCreate):
    orm_item = database.create_item(item=item, owner_id=user.user_id)
    return models.Item.model_validate(orm_item)



class _EditItemRequest(pydantic.BaseModel):
    description: Optional[str] = None
    price_in_cents: Optional[int] = None
    recipient_id: Optional[int] = None
    sales_event_id: Optional[int] = None


@router.put('/items/{item_id}')
def edit_item(database: DatabaseDependency,
              user: Annotated[orm.User, RequireScopes(scopes.Scopes(
                  scopes.EDIT_OWN_ITEM,
              ))],
              item_id: int,
              update: _EditItemRequest):
    orm_item = database.find_item_by_id(id=item_id)
    if orm_item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if orm_item.owner_id != user.user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    for field, value in update:
        if value is not None:
            setattr(orm_item, field, value)
    database.commit()
