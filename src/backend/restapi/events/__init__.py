from fastapi import APIRouter
from . import listevents
from . import addevent
from . import updateevent
from . import items

router = APIRouter(prefix='/events')

router.include_router(listevents.router)
router.include_router(addevent.router)
router.include_router(updateevent.router)
router.include_router(items.router)
