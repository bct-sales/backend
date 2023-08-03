import pydantic
import datetime


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
