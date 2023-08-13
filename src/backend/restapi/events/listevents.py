import datetime
from typing import Annotated

from fastapi import APIRouter
import pydantic

from backend.db.exceptions import *
from backend.restapi.shared import *
from backend.security import scopes


router = APIRouter()


class EventLinks(pydantic.BaseModel):
    edit: str


class Event(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)
    sales_event_id: pydantic.NonNegativeInt
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time
    location: str
    description: str
    links: EventLinks


class SalesLinks(pydantic.BaseModel):
    add: str


class Response(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)
    events: list[Event]
    links: SalesLinks


@router.get('/',
            response_model=Response,
            tags=['events'])
async def get_sales_events(database: DatabaseDependency,
                     user: Annotated[orm.User, RequireScopes(scopes.Scopes(
                        scopes.LIST_SALES_EVENTS,
                    ))]):
    orm_sales_events = database.list_sales_events()
    events = [
        Event(
            sales_event_id=event.sales_event_id,
            date=event.date,
            start_time=event.start_time,
            end_time=event.end_time,
            description=event.description,
            location=event.location,
            links=EventLinks(
                edit=f'/events/{event.sales_event_id}'
            )
        )
        for event in orm_sales_events
    ]
    return Response(
        events=events,
        links=SalesLinks(
            add='/events'
        )
    )
