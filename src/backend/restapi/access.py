from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.database.base import DatabaseSession
from backend.database import models
import backend.security as security
from backend.restapi.shared import *


router = APIRouter()


@router.post("/register", tags=['entry'])
async def register_account(account_registration: models.UserCreate, database: Annotated[DatabaseSession, Depends(get_database)]):
    try:
        database.create_user(account_registration)
        return {"result": "ok"}
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email address already in use")


# @router.post("/login", tags=['entry'])
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], database: Annotated[DatabaseSession, Depends(get_database)]):
#     email_address = form_data.username
#     password = form_data.password

#     try:
#         account = database.login(
#             email_address=email_address,
#             password=password
#         )
#         token = security.create_access_token({'sub': email_address}, scopes=account.role.scopes)

#         return {
#             "access_token": token,
#             "token_type": "bearer",
#         }
#     except UnknownAccountError:
#         raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid email address")
#     except WrongPasswordError:
#         raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid password")
