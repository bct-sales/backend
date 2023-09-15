import subprocess
import pydantic
import uuid
import os


class Item(pydantic.BaseModel):
    item_id: int
    description: str
    price_in_cents: int


class LabelData(pydantic.BaseModel):
    qr_data: str
    description: str
    price_in_cents: int


class SheetSpecifications(pydantic.BaseModel):
    sheet_width: int
    sheet_height: int
    columns: int
    rows: int
    label_width: int
    label_height: int
    corner_radius: int


class LabelGenerationData(pydantic.BaseModel):
    labels: list[LabelData]
    sheet_specs: SheetSpecifications


def generate_label_data_for_item(item: Item) -> LabelData:
    return LabelData(
        qr_data=generate_qr_data_for_item(item),
        description=item.description,
        price_in_cents=item.price_in_cents
    )


def generate_qr_data_for_item(item: Item) -> str:
    return f'{item.price_in_cents}'


def generate_labels(sheet_specifications: SheetSpecifications, items: list[Item]) -> str:
    labels_data = [
        generate_label_data_for_item(item)
        for item in items
    ]
    label_generation_data = LabelGenerationData(labels=labels_data, sheet_specs=sheet_specifications)
    unique_id = uuid.uuid4()
    output_filename = f'{unique_id}.pdf'
    input_path = f'g:/temp/{unique_id}.json'
    output_path = f'g:/temp/{output_filename}'

    with open(input_path, 'w') as f:
        f.write(label_generation_data.model_dump_json())

    environment = os.environ.copy()
    if 'VIRTUAL_ENV' in environment:
        del environment['VIRTUAL_ENV']

    subprocess.Popen([
        'poetry',
        'run',
        'bctqr',
        'generate',
        input_path,
        output_path
    ], cwd=r'G:/repos/bct/bctqr', shell=False, env=environment)

    return output_filename
