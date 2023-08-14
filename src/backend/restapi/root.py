import pydantic
from fastapi import APIRouter, Request


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
            registration=str(request.url_for('register_seller')),
            login=str(request.url_for('login')),
            events=str(request.url_for('list_sales_events')),
        )
    )
    return response
