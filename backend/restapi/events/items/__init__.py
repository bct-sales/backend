from fastapi import APIRouter
from . import listitems
from . import additem
from . import updateitem
from . import deleteitem


router = APIRouter(prefix='/{event_id}/items')

router.include_router(listitems.router)
router.include_router(additem.router)
router.include_router(updateitem.router)
router.include_router(deleteitem.router)
