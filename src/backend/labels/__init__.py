from pathlib import Path
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


def generate_labels(directory: Path, sheet_specifications: SheetSpecifications, items: list[Item]) -> str:
    label_generation_data = build_label_generation_data(sheet_specifications, items)

    unique_id = uuid.uuid4()
    json_filename = f'{unique_id}.json'
    pdf_filename = f'{unique_id}.pdf'
    json_path = directory / json_filename
    pdf_path = directory / pdf_filename

    with open(json_path, 'w') as f:
        f.write(label_generation_data.model_dump_json())

    call_qr_generation_subprocess(json_path, pdf_path)

    return pdf_filename


def build_label_generation_data(sheet_specifications: SheetSpecifications, items: list[Item]) -> LabelGenerationData:
    labels_data = [
        generate_label_data_for_item(item)
        for item in items
    ]
    return LabelGenerationData(labels=labels_data, sheet_specs=sheet_specifications)


def call_qr_generation_subprocess(input_path: Path, output_path: Path):
    environment = os.environ.copy()

    # Needs to be removed otherwise subprocess-poetry will fail to set up correct environment
    if 'VIRTUAL_ENV' in environment:
        del environment['VIRTUAL_ENV']

    command = [
        'poetry',
        'run',
        'bctqr',
        'generate',
        str(input_path.absolute()),
        str(output_path.absolute())
    ]

    subprocess.Popen(command, cwd=r'G:/repos/bct/bctqr', shell=False, env=environment)
