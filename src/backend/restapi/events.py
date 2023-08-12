import datetime
from typing import Annotated, Optional

from fastapi import APIRouter
import pydantic

from backend.db import models
from backend.db.exceptions import *
from backend.restapi.shared import *
from backend.security import scopes


router = APIRouter()


class _GetSalesEventResponse_Event_Links(pydantic.BaseModel):
    edit: str


class _GetSalesEventResponse_Event(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)
    sales_event_id: int
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time
    location: str
    description: str
    links: _GetSalesEventResponse_Event_Links


class _GetSalesEventResponse_Links(pydantic.BaseModel):
    add: str

class _GetSalesEventResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)
    events: list[_GetSalesEventResponse_Event]
    links: _GetSalesEventResponse_Links


@router.get('/', response_model=_GetSalesEventResponse)
def get_sales_events(database: DatabaseDependency,
                     user: Annotated[orm.User, RequireScopes(scopes.Scopes(
                        scopes.LIST_SALES_EVENTS,
                    ))]):
    orm_sales_events = database.list_sales_events()
    events = [
        _GetSalesEventResponse_Event(
            sales_event_id=event.sales_event_id,
            date=event.date,
            start_time=event.start_time,
            end_time=event.end_time,
            description=event.description,
            location=event.location,
            links=_GetSalesEventResponse_Event_Links(
                edit=f'/events/{event.sales_event_id}'
            )
        )
        for event in orm_sales_events
    ]
    return _GetSalesEventResponse(
        events=events,
        links=_GetSalesEventResponse_Links(
            add='/events'
        )
    )


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=models.SalesEvent)
def add_sales_event(event_data: models.SalesEventCreate,
                    database: DatabaseDependency,
                    user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.ADD_SALES_EVENTS))]):
    orm_sales_event = database.create_sales_event(event_data)
    return models.SalesEvent.model_validate(orm_sales_event)



class _UpdateSalesPayload(pydantic.BaseModel):
    date: Optional[datetime.date] = None
    start_time: Optional[datetime.time] = None
    end_time: Optional[datetime.time] = None
    location: Optional[str] = None
    description: Optional[str] = None


@router.put('/{sales_event_id}')
def update_sales_event(database: DatabaseDependency,
                       payload: _UpdateSalesPayload,
                       sales_event_id: int,
                       user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.EDIT_SALES_EVENT))]):
    orm_sales_event = database.find_sales_event_by_id(sales_event_id)
    if orm_sales_event is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    for field, value in payload:
        if value:
            setattr(orm_sales_event, field, value)
    database.commit()
