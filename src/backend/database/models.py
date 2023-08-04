import pydantic
import datetime


class UserBase(pydantic.BaseModel):
    email_address: str
    role: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    model_config = pydantic.ConfigDict(from_attributes=True)
    user_id: int
    password_hash: str


class SaleBase(pydantic.BaseModel):
    date: datetime.date


class SaleCreate(SaleBase):
    pass


class Sale(SaleBase):
    model_config = pydantic.ConfigDict(from_attributes=True)

    sale_id: int


class ItemBase(pydantic.BaseModel):
    description: str
    price_in_cents: pydantic.NonNegativeInt


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    model_config = pydantic.ConfigDict(from_attributes=True)

    item_id: int
