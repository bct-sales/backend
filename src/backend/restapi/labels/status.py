from pathlib import Path
from typing import Annotated, Literal
from fastapi import APIRouter, HTTPException, Request
from backend.db import orm
from backend.labels import is_labels_generation_ready, is_valid_labels_id
from backend.restapi.labels.util import get_labels_generation_directory
from backend.restapi.shared import RequireScopes
from backend.security import scopes
from fastapi import status
import pydantic

from backend.util import url_for



router = APIRouter()


class ReadyStatusResponse(pydantic.BaseModel):
    status: Literal['ready'] = 'ready'
    url: str


class PendingStatusResponse(pydantic.BaseModel):
    status: Literal['pending'] = 'pending'


StatusResponse = ReadyStatusResponse | PendingStatusResponse


@router.get('/status/{labels_id}',
            tags=['labels'],
            response_model=StatusResponse)
async def label_generation_status(request: Request,
                                  user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.LIST_OWN_ITEMS))],
                                  labels_id: str):
    if not is_valid_labels_id(labels_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    directory = get_labels_generation_directory()
    if is_labels_generation_ready(directory, labels_id):
        url = url_for(request, 'download_labels', labels_id=labels_id)
        return ReadyStatusResponse(url=str(url))
    else:
        return PendingStatusResponse()
