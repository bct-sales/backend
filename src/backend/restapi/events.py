from typing import Annotated, Optional

from fastapi import APIRouter
import pydantic

from backend.db import models
from backend.db.exceptions import *
from backend.restapi.shared import *
from backend.security import scopes


router = APIRouter()

@router.get('/', response_model=list[models.SalesEvent])
def get_sales_events(database: DatabaseDependency,
                     user: Annotated[orm.User, RequireScopes(scopes.Scopes(
                        scopes.LIST_SALES_EVENTS,
                    ))]):
    orm_sales_events = database.list_sales_events()
    return [models.SalesEvent.model_validate(event) for event in orm_sales_events]


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=models.SalesEvent)
def add_sales_event(event_data: models.SalesEventCreate,
                    database: DatabaseDependency,
                    user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.ADD_SALES_EVENTS))]):
    orm_sales_event = database.create_sales_event(event_data)
    return models.SalesEvent.model_validate(orm_sales_event)



class _UpdateSalesPayload(pydantic.BaseModel):
    date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
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
        setattr(orm_sales_event, field, value)
    database.commit()
