from fastapi import APIRouter
from fastapi.responses import FileResponse

from backend.db.exceptions import *
from backend.restapi.shared import *
import backend.db.orm as orm


router = APIRouter()


class LabelData(pydantic.BaseModel):
    qr_data: str
    description: str
    price_in_cents: int


class LabelGenerationData(pydantic.BaseModel):
    labels: list[LabelData]


@router.post('/generate',
             tags=['labels'])
async def generate(database: DatabaseDependency,
                   user: Annotated[orm.User, RequireScopes(scopes.Scopes(scopes.LIST_OWN_ITEMS))],
                   event_id: int):
    orm_items = database.list_items_owned_by(owner=user.user_id, sale_event=event_id)
    labels_data = [
        generate_label_data_for_item(item)
        for item in orm_items
    ]
    label_generation_data = LabelGenerationData(labels=labels_data)
    return label_generation_data.model_dump() # TODO


def generate_label_data_for_item(item: orm.Item) -> LabelData:
    return LabelData(
        qr_data=generate_qr_data_for_item(item),
        description=item.description,
        price_in_cents=item.price_in_cents
    )


def generate_qr_data_for_item(item: orm.Item) -> str:
    return f'{item.price_in_cents}'
