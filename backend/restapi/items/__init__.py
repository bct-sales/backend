from fastapi import APIRouter

from backend.db.exceptions import *

from . import get


router = APIRouter(prefix='/items')

router.include_router(get.router)
