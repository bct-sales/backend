from typing import Annotated
from fastapi import APIRouter, Depends
import pydantic

from backend.database.base import DatabaseSession
from backend.restapi.shared import database_dependency


router = APIRouter(
    tags=['users']
)
