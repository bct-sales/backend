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


class User(pydantic.BaseModel):
    id: str
    scopes: list[str]

def get_user() -> User:
    return User(id='jos', scopes=['a', 'b', 'c'])

def RequiresScopes(*scopes: str) -> Any:
    def dependency(user: User = Depends(get_user)):
        if not set(scopes) <= set(user.scopes):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        return user
    return Depends(dependency)


@router.get("/items", response_model=list[_Item])
async def list_items(database: DatabaseDependency):
    return database.list_items()
