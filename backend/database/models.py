import pydantic


class Item(pydantic.BaseModel):
    description: str
    price_in_cents: pydantic.NonNegativeInt
