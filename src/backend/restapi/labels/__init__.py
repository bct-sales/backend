from fastapi import APIRouter
from fastapi.responses import FileResponse

from backend.db.exceptions import *
from backend.restapi.shared import *


router = APIRouter(prefix='/labels')


@router.get('/{id}/labels.pdf',
            tags=['qr'],
            response_class=FileResponse)
async def download(id: str):
    return FileResponse("g:/fiche2.pdf")
