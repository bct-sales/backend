from fastapi import APIRouter
from . import login
from . import register


router = APIRouter()

router.include_router(login.router)
router.include_router(register.router)
