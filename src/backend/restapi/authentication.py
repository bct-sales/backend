from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.database import models
import backend.security as security
from backend.restapi.shared import *
from backend.database.exceptions import *
from backend.security.scopes import Scopes



router = APIRouter()


@router.post("/register", tags=['authentication'])
async def register_account(account_registration: models.UserCreate, database: DatabaseDependency):
    try:
        database.create_user(account_registration)
        return {"result": "ok"}
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email address already in use")


@router.post("/login", tags=['authentication'])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], database: DatabaseDependency):
    email_address = form_data.username
    password = form_data.password

    try:
        user = database.login(
            email_address=email_address,
            password=password
        )
        role = Role.from_name(user.role)
        token_data = security.TokenData(email_address=email_address, scopes=role.scopes)
        token = security.create_access_token(token_data=token_data)

        return {
            "access_token": token,
            "token_type": "bearer",
        }
    except UnknownUserException:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No user with this email address")
    except WrongPasswordException:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Wrong password")
