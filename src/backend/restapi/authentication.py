from fastapi import APIRouter
from typing import Annotated, Literal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.db import models
import backend.security as security
from backend.restapi.shared import *
from backend.db.exceptions import *
from backend.security import roles

import pydantic
import logging


router = APIRouter()


class _RegisterSellerData(pydantic.BaseModel):
    email_address: str
    password: str


@router.post("/register", tags=['authentication'], status_code=status.HTTP_201_CREATED)
async def register_seller(seller_creation_data: _RegisterSellerData, database: DatabaseDependency):
    user_creation_data = models.UserCreate(
        email_address=seller_creation_data.email_address,
        role=roles.SELLER.name,
        password=seller_creation_data.password
    )
    try:
        database.create_user(user_creation_data)
        return {"result": "ok"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))


class _LoginResponse(pydantic.BaseModel):
    access_token: str
    role: str
    token_type: Literal["bearer"]

@router.post("/login", tags=['authentication'], response_model=_LoginResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], database: DatabaseDependency):
    email_address = form_data.username
    password = form_data.password

    try:
        user = database.login(
            email_address=email_address,
            password=password
        )
        role = Role.from_name(user.role)
        logging.debug(f'User {email_address} logged in, role {role}')
        token_data = security.TokenData(user_id=user.user_id, scopes=role.scopes)
        token = security.create_access_token(token_data=token_data)

        return _LoginResponse(
            access_token=token,
            role=role.name,
            token_type="bearer",
        )

    except UnknownUserException:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No user with this email address")
    except WrongPasswordException:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Wrong password")
