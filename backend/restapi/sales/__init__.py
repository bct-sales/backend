from fastapi import APIRouter

from backend.db.exceptions import *

from . import registersale


router = APIRouter(prefix='/sales')

router.include_router(registersale.router)
