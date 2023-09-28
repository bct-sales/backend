from pathlib import Path
import subprocess
import pydantic
import logging
import uuid
import os

from backend import settings


class Item(pydantic.BaseModel):
    item_id: int
    description: str
    price_in_cents: int
    charity: bool
    owner_id: int
    recipient_id: int


class LabelData(pydantic.BaseModel):
    qr_data: str
    description: str
    price_in_cents: int
    charity: bool
    item_id: int
    owner_id: int
    recipient_id: int


class SheetSpecifications(pydantic.BaseModel):
    sheet_width: int
    sheet_height: int
    columns: int
    rows: int
    label_width: int
    label_height: int
    corner_radius: int
    margin: int
    spacing: int
    font_size: int
    border: bool


class LabelGenerationData(pydantic.BaseModel):
    labels: list[LabelData]
    sheet_specs: SheetSpecifications


def generate_label_data_for_item(item: Item) -> LabelData:
    return LabelData(
        qr_data=generate_qr_data_for_item(item),
        description=item.description,
        price_in_cents=item.price_in_cents,
        charity=item.charity,
        item_id=item.item_id,
        owner_id=item.owner_id,
        recipient_id=item.recipient_id,
    )


def generate_qr_data_for_item(item: Item) -> str:
    string = f'P{item.price_in_cents}R{item.recipient_id}I{item.item_id}'
    if item.charity:
        string += 'C'
    return string


def generate_labels(directory: Path, sheet_specifications: SheetSpecifications, items: list[Item]) -> str:
    label_generation_data = build_label_generation_data(sheet_specifications, items)

    unique_id = uuid.uuid4()
    json_path = directory / f'{unique_id}.json'
    pdf_path = directory / f'{unique_id}.pdf'

    with open(json_path, 'w') as f:
        f.write(label_generation_data.model_dump_json())

    call_qr_generation_subprocess(json_path, pdf_path)

    return str(unique_id)


def is_valid_labels_id(id: str) -> bool:
    try:
        uuid.UUID(id)
        return True
    except ValueError:
        return False


def is_labels_generation_ready(directory: Path, id: str) -> bool:
    if not is_valid_labels_id(id):
        return False
    path = directory / f'{str(id)}.pdf'
    return path.is_file()


def build_label_generation_data(sheet_specifications: SheetSpecifications, items: list[Item]) -> LabelGenerationData:
    labels_data = [
        generate_label_data_for_item(item)
        for item in items
    ]
    return LabelGenerationData(labels=labels_data, sheet_specs=sheet_specifications)


def call_qr_generation_subprocess(input_path: Path, output_path: Path):
    logging.info('Creating QR generation subprocess')
    environment = os.environ.copy()

    # Needs to be removed otherwise subprocess-poetry will fail to set up correct environment
    if 'VIRTUAL_ENV' in environment:
        del environment['VIRTUAL_ENV']

    cfg = settings.load_settings()
    qr_directory = cfg.qr_directory

    command = [
        'poetry',
        'run',
        'bctqr',
        'generate',
        str(input_path.absolute()),
        str(output_path.absolute())
    ]

    subprocess.Popen(command, cwd=qr_directory, shell=False, env=environment)
