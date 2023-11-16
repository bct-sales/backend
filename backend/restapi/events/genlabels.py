from typing import Annotated
from fastapi import APIRouter, Request
from backend.db import orm
from backend.labels import generate_labels, SheetSpecifications,Item
from backend.restapi.labels.util import get_labels_generation_directory
from backend.restapi.shared import DatabaseDependency, RequireScopes
from backend.security import scopes
import pydantic

from backend.util import url_for



router = APIRouter()

class GenerateData(pydantic.BaseModel):
    sheet_width: int
    sheet_height: int
    columns: int
    rows: int
    label_width: float
    label_height: float
    corner_radius: int
    margin: int
    spacing: int
    font_size: int
    border: bool
    left_margin: float
    right_margin: float
    top_margin: float
    bottom_margin: float


class GenerateResponse(pydantic.BaseModel):
    status_url: str


@router.post('/{event_id}/generate',
             tags=['labels'])
async def generate_labels_for_event(request: Request,
                                    database: DatabaseDependency,
                                    user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.LIST_OWN_ITEMS))],
                                    event_id: int,
                                    payload: GenerateData):
    orm_items = database.list_items_owned_by(owner=user.user_id, sale_event=event_id)
    items = [
        Item(
            item_id=orm_item.item_id,
            description=orm_item.description,
            category=orm_item.category,
            price_in_cents=orm_item.price_in_cents,
            charity=orm_item.charity,
            owner_id=orm_item.owner_id,
            recipient_id=orm_item.recipient_id,
        )
        for orm_item in orm_items
    ]
    sheet_specifications = SheetSpecifications(
        sheet_width=payload.sheet_width,
        sheet_height=payload.sheet_height,
        columns=payload.columns,
        rows=payload.rows,
        label_width=payload.label_width,
        label_height=payload.label_height,
        corner_radius=payload.corner_radius,
        margin=payload.margin,
        spacing=payload.spacing,
        font_size=payload.font_size,
        border=payload.border,
        left_margin=payload.left_margin,
        right_margin=payload.right_margin,
        top_margin=payload.top_margin,
        bottom_margin=payload.bottom_margin,
    )

    directory = get_labels_generation_directory()
    download_id = generate_labels(directory, sheet_specifications, items)

    status_url = url_for(request, 'label_generation_status', labels_id=download_id)
    return GenerateResponse(status_url=str(status_url)).model_dump()
