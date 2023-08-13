from fastapi import APIRouter
from . import authentication
from . import register


router = APIRouter()

router.include_router(authentication.router)
router.include_router(register.router)
