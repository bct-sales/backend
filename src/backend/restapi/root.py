import pydantic
from fastapi import APIRouter, Request

from backend.util import url_for


router = APIRouter()


class Links(pydantic.BaseModel):
    registration: str
    login: str
    events: str


class Response(pydantic.BaseModel):
    links: Links


@router.get('/', tags=['root'])
async def root(request: Request):
    """
    Starting point of REST API
    """
    response = Response(
        links=Links(
            registration=url_for(request, 'register_seller'),
            login=url_for(request, 'login'),
            events=url_for(request, 'list_sales_events'),
        )
    )
    return response
