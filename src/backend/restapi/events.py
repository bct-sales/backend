from typing import Annotated

from fastapi import APIRouter

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


@router.post('/')
def add_sales_event(event_data: models.SalesEventCreate,
                    database: DatabaseDependency,
                    user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.ADD_SALES_EVENTS))]):
    database.create_sales_event(event_data)
