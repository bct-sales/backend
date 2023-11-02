from fastapi import APIRouter, status
from fastapi.responses import FileResponse

from backend.db.exceptions import *
from backend.restapi.shared import *
import backend.db.orm as orm
import pydantic


router = APIRouter()


class Response(pydantic.BaseModel):
    item_ids: list[int]


@router.get('/',
            tags=['items'],
            response_model=Response)
async def list_items(database: DatabaseDependency,
                    user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.LIST_ALL_ITEMS))]):
    items = database.list_items()
    item_ids = [item.item_id for item in items]
    response = Response(
        item_ids=item_ids
    )
    return response
