from fastapi import APIRouter, Request
from fastapi import Depends, HTTPException, status
from backend.db import models
from backend.restapi.shared import *
from backend.db.exceptions import *
from backend.security import roles

import pydantic
import logging


router = APIRouter()


class SellerRegistrationData(pydantic.BaseModel):
    email_address: pydantic.EmailStr
    password: str


@router.post("/register",
             tags=['authentication'],
             status_code=status.HTTP_201_CREATED)
async def register_seller(seller_creation_data: SellerRegistrationData,
                          database: DatabaseDependency):
    user_creation_data = models.UserCreate(
        email_address=seller_creation_data.email_address,
        role=roles.SELLER.name,
        password=seller_creation_data.password
    )
    try:
        database.create_user(user_creation_data)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
