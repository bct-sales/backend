from fastapi import APIRouter
from backend.restapi import authentication
from backend.restapi import events
from backend.restapi import root


router = APIRouter(prefix="/api/v1")

router.include_router(root.router)
router.include_router(authentication.router)
router.include_router(events.router)
