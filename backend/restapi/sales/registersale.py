from fastapi import APIRouter, status

from backend.db.exceptions import *
from backend.restapi.shared import *
import backend.db.orm as orm
import pydantic


router = APIRouter()


class Payload(pydantic.BaseModel):
    item_ids: list[int]


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             tags=['sales'])
async def register_sale(sale_data: Payload,
                        database: DatabaseDependency,
                        user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.REGISTER_SALE))]):
    try:
        database.create_sale(sale_data.item_ids)
    except EmptySaleIsInvalid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Sale must contain at least one item')
    except DuplicateItemsInSale:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Duplicate items in sale')
    except UnknownItemException:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Unknown item')
