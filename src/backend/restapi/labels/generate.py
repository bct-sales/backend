from typing import Annotated
from fastapi import APIRouter, Request
from backend.db import orm
from backend.labels import generate_labels, SheetSpecifications,Item
from backend.restapi.labels.util import determine_user_specific_directory
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
    status_url: str


@router.post('/generate',
             tags=['labels'])
async def generate(request: Request,
                   database: DatabaseDependency,
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

    directory = determine_user_specific_directory(user.user_id)
    download_id = generate_labels(directory, sheet_specifications, items)

    status_url = request.url_for('label_generation_status', labels_id=download_id)
    return GenerateResponse(status_url=str(status_url)).model_dump()
