from typing import Annotated, Optional

from fastapi import APIRouter
import pydantic

from backend.db import models
from backend.db.exceptions import *
from backend.restapi.shared import *
from backend.security import scopes


router = APIRouter()


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             response_model=models.SalesEvent,
             tags=['events'])
async def add_sales_event(event_data: models.SalesEventCreate,
                    database: DatabaseDependency,
                    user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.ADD_SALES_EVENTS))]):
    orm_sales_event = database.create_sales_event(event_data)
    return models.SalesEvent.model_validate(orm_sales_event)
