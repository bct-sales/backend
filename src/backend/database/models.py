import pydantic
import datetime


class UserBase(pydantic.BaseModel):
    email_address: str
    password_hash: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_id: int


class SaleBase(pydantic.BaseModel):
    date: datetime.date


class SaleCreate(SaleBase):
    pass


class Sale(SaleBase):
    sale_id: int


class ItemBase(pydantic.BaseModel):
    description: str
    price_in_cents: pydantic.NonNegativeInt


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    item_id: int
