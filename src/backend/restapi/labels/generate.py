from typing import Annotated
from fastapi import APIRouter
from backend.db import orm
from backend.labels import generate_labels, SheetSpecifications,Item
from backend.restapi.shared import DatabaseDependency, RequireScopes
from backend.security import scopes
import pydantic


router = APIRouter()

class GenerateData(pydantic.BaseModel):
    sheet_width: int
    sheet_height: int
    columns: int
    rows: int
    label_width: int
    label_height: int
    corner_radius: int


class GenerateResponse(pydantic.BaseModel):
    filename: str


@router.post('/generate',
             tags=['labels'])
async def generate(database: DatabaseDependency,
                   user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.LIST_OWN_ITEMS))],
                   event_id: int,
                   payload: GenerateData):
    orm_items = database.list_items_owned_by(owner=user.user_id, sale_event=event_id)
    items = [
        Item(
            item_id=orm_item.item_id,
            description=orm_item.description,
            price_in_cents=orm_item.price_in_cents
        )
        for orm_item in orm_items
    ]
    sheet_specifications = SheetSpecifications(**payload.model_dump())
    filename = generate_labels(sheet_specifications, items)
    return GenerateResponse(filename=filename).model_dump()
