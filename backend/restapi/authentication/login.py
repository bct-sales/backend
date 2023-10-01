from fastapi import APIRouter, Request
from typing import Annotated, Literal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.db import models
import backend.security as security
from backend.restapi.shared import *
from backend.db.exceptions import *

import pydantic
import logging

from backend.security.roles import Role


router = APIRouter()


class Links(pydantic.BaseModel):
    events: str

class Response(pydantic.BaseModel):
    user_id: pydantic.NonNegativeInt
    access_token: str
    role: Literal['seller', 'admin', 'cashier']
    token_type: Literal["bearer"]
    links: Links


@router.post("/login",
             tags=['authentication'],
             response_model=Response)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                database: DatabaseDependency):
    user_id_string = form_data.username
    password = form_data.password

    try:
        user_id = int(user_id_string)
    except ValueError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"{user_id_string!r} is not a valid user id"
        )

    try:
        user = database.login_with_id(
            user_id=user_id,
            password=password
        )
        role = Role.from_name(user.role)
        logging.debug(f'User {user_id} logged in, role {role}')
        token_data = security.TokenData(user_id=user.user_id, scopes=role.scopes)
        token = security.create_access_token(token_data=token_data)

        return Response(
            user_id=user.user_id,
            access_token=token,
            role=role.name,
            token_type="bearer",
            links=Links(
                events='/events'
            )
        )
    except UnknownUserException:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"No user with id {user_id}"
        )
    except WrongPasswordException:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Wrong password"
        )
