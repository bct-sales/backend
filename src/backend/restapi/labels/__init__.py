from fastapi import APIRouter

from backend.db.exceptions import *
from backend.restapi.shared import RequireScopes, DatabaseDependency

from . import generate
from . import download
from . import status

router = APIRouter(prefix='/labels')


router.include_router(generate.router)
router.include_router(download.router)
router.include_router(status.router)
