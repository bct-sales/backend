import pydantic
from fastapi import APIRouter


router = APIRouter()


class Links(pydantic.BaseModel):
    registration: str
    login: str


class Response(pydantic.BaseModel):
    links: Links


@router.get('/', tags=['root'])
async def root():
    response = Response(
        links=Links(
            registration='/register',
            login='/login',
        )
    )
    return response
