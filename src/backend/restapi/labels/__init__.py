from fastapi import APIRouter

from backend.db.exceptions import *
from backend.restapi.shared import *

from . import generate
from . import download

router = APIRouter(prefix='/labels')


router.include_router(generate.router)
router.include_router(download.router)
