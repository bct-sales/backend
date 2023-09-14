from fastapi import APIRouter

from backend.restapi import authentication, events, labels, root

router = APIRouter(prefix="/api/v1")

router.include_router(root.router)
router.include_router(authentication.router)
router.include_router(events.router)
router.include_router(labels.router)
