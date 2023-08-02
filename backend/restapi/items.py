from typing import Annotated
from fastapi import APIRouter, Depends
import pydantic
import logging

from backend.database.base import Database
from backend.database.memorydb import InMemoryDatabase


router = APIRouter(
    tags=['items']
)


def create_database() -> Database:
    return InMemoryDatabase()


class _Item(pydantic.BaseModel):
    description: str
    price_in_cents: pydantic.NonNegativeInt


@router.get("/items", response_model=list[_Item])
async def list_users_items(database: Annotated[Database, Depends(create_database)]):
    items = database.list_items()
    return items
