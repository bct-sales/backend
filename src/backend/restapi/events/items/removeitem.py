from typing import Annotated

import pydantic
from fastapi import APIRouter, Depends

from backend.db import models
from backend.restapi.shared import *

router = APIRouter()


@router.delete("/{item_id}",
               tags=['items'])
async def remove_item(database: DatabaseDependency,
                      user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.REMOVE_OWN_ITEM))],
                      event_id: int):
    # TODO
    pass
