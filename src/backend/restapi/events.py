from typing import Annotated

from fastapi import APIRouter

from backend.database import models
from backend.database.exceptions import *
from backend.restapi.shared import *
from backend.security import scopes


router = APIRouter()

@router.get('/', response_model=list[models.SalesEvent])
def get_sales_events(database: DatabaseDependency,
                     user: Annotated[orm.User, RequireScopes(scopes.Scopes(
                        scopes.LIST_SALES_EVENTS,
                    ))]):
    orm_sales_events = database.list_sales_events()
    return orm_sales_events
