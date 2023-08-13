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
    """
    Starting point of REST API
    """
    response = Response(
        links=Links(
            registration='/register',
            login='/login',
        )
    )
    return response
