import datetime
from typing import Annotated, Optional

from fastapi import APIRouter
import pydantic

from backend.db import models
from backend.db.exceptions import *
from backend.restapi.shared import *
from backend.security import scopes


router = APIRouter()


class UpdateSalesData(pydantic.BaseModel):
    date: Optional[datetime.date] = None
    start_time: Optional[datetime.time] = None
    end_time: Optional[datetime.time] = None
    location: Optional[str] = None
    description: Optional[str] = None
    available: Optional[bool] = None


@router.put('/{event_id}', tags=['events'])
async def update_sales_event(database: DatabaseDependency,
                             payload: UpdateSalesData,
                             event_id: int,
                             user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.EDIT_SALES_EVENT))]):
    try:
        database.update_event(id=event_id, **dict(payload))
    except UnknownSalesEventException:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
