import pydantic
import datetime


class UserBase(pydantic.BaseModel):
    email_address: str
    role: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    model_config = pydantic.ConfigDict(from_attributes=True)
    user_id: pydantic.NonNegativeInt
    password_hash: str


class SalesEventBase(pydantic.BaseModel):
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time
    location: str
    description: str
    available: bool


class SalesEventCreate(SalesEventBase):
    pass


class SalesEvent(SalesEventBase):
    model_config = pydantic.ConfigDict(from_attributes=True)
    sales_event_id: pydantic.NonNegativeInt


class ItemBase(pydantic.BaseModel):
    description: str
    price_in_cents: pydantic.NonNegativeInt
    recipient_id: pydantic.NonNegativeInt
    sales_event_id: pydantic.NonNegativeInt
    owner_id: pydantic.NonNegativeInt
    charity: pydantic.StrictBool


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    model_config = pydantic.ConfigDict(from_attributes=True)
    item_id: pydantic.NonNegativeInt
