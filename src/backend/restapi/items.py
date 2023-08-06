from typing import Annotated, Any

import pydantic
from fastapi import APIRouter, Depends
from backend.database import models

from backend.restapi.shared import *
from backend.security.scopes import Scopes


router = APIRouter(
    tags=['items']
)


class _Item(pydantic.BaseModel):
    description: str
    price_in_cents: pydantic.NonNegativeInt


@router.get("/items", response_model=list[_Item])
async def list_items(database: DatabaseDependency):
    return database.list_items()
