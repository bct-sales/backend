from fastapi import APIRouter
from fastapi.responses import FileResponse

from backend.db.exceptions import *
from backend.restapi.shared import *
import backend.db.orm as orm


router = APIRouter()


@router.get('/{id}/labels.pdf',
            tags=['labels'],
            response_class=FileResponse)
async def download(id: str):
    return FileResponse("g:/fiche2.pdf")
