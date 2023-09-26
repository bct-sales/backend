from pathlib import Path

from backend.settings import load_settings


def get_labels_generation_directory() -> Path:
    directory = Path(load_settings().label_generation_directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory
