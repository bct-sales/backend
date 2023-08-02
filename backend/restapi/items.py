from typing import Any
from fastapi import APIRouter
import pydantic


router = APIRouter(
    tags=['items']
)


class _GetItemResponse(pydantic.BaseModel):
    name: str


@router.get("/item")
async def list_users_items():
    return _GetItemResponse(name="hello")
