from fastapi import APIRouter, status
from fastapi.responses import FileResponse

from backend.db.exceptions import *
from backend.labels import is_valid_labels_id
from backend.restapi.labels.util import get_labels_generation_directory
from backend.restapi.shared import *
import backend.db.orm as orm
import pydantic


router = APIRouter()


class Response(pydantic.BaseModel):
    item_id: int
    description: str
    category: str
    price_in_cents: pydantic.NonNegativeInt
    recipient_id: pydantic.NonNegativeInt
    sales_event_id: pydantic.NonNegativeInt
    owner_id: pydantic.NonNegativeInt
    charity: pydantic.StrictBool


# TODO Require cashier role

@router.get('/{item_id}',
            tags=['items'],
            response_model=Response)
async def download_labels(item_id: int,
                          database: DatabaseDependency):
    orm_item = database.find_item_by_id(item_id)
    if orm_item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    response = Response(
        item_id=orm_item.item_id,
        description=orm_item.description,
        category=orm_item.category,
        price_in_cents=orm_item.price_in_cents,
        recipient_id=orm_item.recipient_id,
        sales_event_id=orm_item.sales_event_id,
        owner_id=orm_item.owner_id,
        charity=orm_item.charity,
    )
    return response
