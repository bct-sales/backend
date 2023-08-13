import datetime
from typing import Annotated, Optional

from fastapi import APIRouter
import pydantic

from backend.db import models
from backend.db.exceptions import *
from backend.restapi.shared import *
from backend.security import scopes


router = APIRouter()


class _UpdateSalesPayload(pydantic.BaseModel):
    date: Optional[datetime.date] = None
    start_time: Optional[datetime.time] = None
    end_time: Optional[datetime.time] = None
    location: Optional[str] = None
    description: Optional[str] = None


@router.put('/{event_id}', tags=['events'])
def update_sales_event(database: DatabaseDependency,
                       payload: _UpdateSalesPayload,
                       event_id: int,
                       user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.EDIT_SALES_EVENT))]):
    orm_sales_event = database.find_sales_event_by_id(event_id)
    if orm_sales_event is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    for field, value in payload:
        if value:
            setattr(orm_sales_event, field, value)
    database.commit()
