from pathlib import Path

from backend.settings import load_settings


def determine_user_specific_directory(user_id: int) -> Path:
    directory = Path(load_settings().label_generation_directory) / str(user_id)
    directory.mkdir(parents=True, exist_ok=True)
    return directory
