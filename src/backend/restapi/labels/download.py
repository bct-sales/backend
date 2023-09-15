from fastapi import APIRouter, status
from fastapi.responses import FileResponse

from backend.db.exceptions import *
from backend.labels import is_valid_labels_id
from backend.restapi.labels.util import determine_user_specific_directory
from backend.restapi.shared import *
import backend.db.orm as orm


router = APIRouter()


@router.get('/download/{labels_id}/labels.pdf',
            tags=['labels'],
            response_class=FileResponse)
async def download_labels(labels_id: str,
                          user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.LIST_OWN_ITEMS))]):
    if not is_valid_labels_id(labels_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    directory = determine_user_specific_directory(user.user_id)
    path = directory / f'{labels_id}.pdf'
    return FileResponse(path)
