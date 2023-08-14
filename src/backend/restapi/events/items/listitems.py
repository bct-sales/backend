from typing import Annotated, Any, Optional

import pydantic
from fastapi import APIRouter, Depends, Request
from backend.db import models

from backend.restapi.shared import *
from backend.security.scopes import Scopes


router = APIRouter()


class ItemLinks(pydantic.BaseModel):
    edit: str


class Item(models.Item):
    model_config = pydantic.ConfigDict(from_attributes=True)

    links: ItemLinks


class Links(pydantic.BaseModel):
    add: str


class Response(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    items: list[Item]
    links: Links


@router.get("/",
            response_model=Response,
            tags=['items'])
async def list_items(request: Request,
                     event_id: int,
                     database: DatabaseDependency,
                     user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.LIST_OWN_ITEMS))]):
    orm_items = database.list_items_owned_by(owner=user.user_id, sale_event=event_id)
    items = [
        Item(
            description=item.description,
            item_id=item.item_id,
            owner_id=item.owner_id,
            links=ItemLinks(
                edit=str(request.url_for("update_item", event_id=event_id, item_id=item.item_id)),
            ),
            recipient_id=item.recipient_id,
            price_in_cents=item.price_in_cents,
            sales_event_id=item.sales_event_id,
        )
        for item in orm_items
    ]
    return Response(
        items=items,
        links=Links(
            add=str(request.url_for('list_items', event_id=event_id)),
        )
    )
