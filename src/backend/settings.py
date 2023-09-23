import logging
from typing import Optional
import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='BCT_', env_file='.env', env_file_encoding='utf-8')

    # Allowed to be None for tests (in memory DB)
    database_path: Optional[str] = None

    jwt_secret_key: str = ""

    jwt_algorithm: str = 'HS256'

    jwt_expiration: int = 6 * 60 # 6 Hours

    label_generation_directory: str = ""

    # Path where index.html is stored locally
    html_path: str = ''

    # URL where latest version of index.html can be found
    html_url: str = 'https://github.com/bct-sales/frontend/releases/latest/download/index.html'

    @pydantic.computed_field # type: ignore[misc]
    @property
    def database_url(self) -> str:
        if self.database_path:
            return f'sqlite:///{self.database_path}'
        else:
            return 'sqlite:///'


_settings: Optional[Settings] = None


def verify_settings(settings: Settings):
    if len(settings.jwt_secret_key) == 0:
        logging.critical("No JWT key found!")
        raise RuntimeError("No JWT key found")
    if len(settings.html_path) == 0:
        logging.critical("No HTML path set!")
        raise RuntimeError("No HTML path set")
    if not os.path.isfile(settings.html_path):
        logging.critical(f"No HTML found at {settings.html_path}!")
        raise RuntimeError(f"HTML file not found at {settings.html_path}")
    if len(settings.label_generation_directory) == 0:
        logging.critical("No label generation directory set!")
        raise RuntimeError("No label generation directory set!")
    if not os.path.isdir(settings.label_generation_directory):
        logging.critical(f"Label generation directory {settings.label_generation_directory} does not exist!")
        raise RuntimeError(f"Label generation directory {settings.label_generation_directory} does not exist!")


def load_settings(verify=True) -> Settings:
    global _settings
    if _settings is None:
        # Parameter necessary to keep linter from complaining
        _settings = Settings(**{})
    if verify:
        verify_settings(_settings)

    # Expand ~
    if _settings.database_path:
        _settings.database_path = os.path.expanduser(_settings.database_path)
    _settings.html_path = os.path.expanduser(_settings.html_path)
    _settings.label_generation_directory = os.path.expanduser(_settings.label_generation_directory)

    return _settings
