from typing import Annotated
from fastapi import APIRouter, Depends
import pydantic

from backend.database.base import DatabaseSession
from backend.restapi.shared import database_dependency


router = APIRouter(
    tags=['items']
)


class _Item(pydantic.BaseModel):
    description: str
    price_in_cents: pydantic.NonNegativeInt


@router.get("/items", response_model=list[_Item])
async def list_users_items(database: Annotated[DatabaseSession, Depends(database_dependency)]):
    return database.list_items()
