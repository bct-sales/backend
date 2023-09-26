from typing import Annotated

from fastapi import APIRouter, HTTPException, status

from backend.restapi.shared import *


router = APIRouter()

@router.delete("/{item_id}",
               tags=['items'])
async def delete_item(database: DatabaseDependency,
                      user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.REMOVE_OWN_ITEM))],
                      item_id: int):
    item_to_be_deleted = database.find_item_by_id(item_id)
    if item_to_be_deleted is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if item_to_be_deleted.owner_id != user.user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    database.delete_item_by_id(item_id)
