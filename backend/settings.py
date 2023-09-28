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


def verify_settings(settings: Settings) -> None:
    if len(settings.jwt_secret_key) == 0:
        message = "No JWT key found! Set BCT_JWT_SECRET_KEY"
        logging.critical(message)
        raise RuntimeError(message)
    if len(settings.html_path) == 0:
        message = "No HTML path set! Set BCT_HTML_PATH"
        logging.critical(message)
        raise RuntimeError(message)
    if not os.path.isfile(settings.html_path):
        message = f"No HTML found at {settings.html_path}!"
        logging.critical(message)
        raise RuntimeError(message)
    if len(settings.label_generation_directory) == 0:
        message = "No label generation directory set!"
        logging.critical(message)
        raise RuntimeError(message)
    if not os.path.isdir(settings.label_generation_directory):
        message = f"Label generation directory {settings.label_generation_directory} does not exist!"
        logging.critical(message)
        raise RuntimeError(message)


def expand_paths(settings: Settings) -> None:
    if settings.database_path:
        settings.database_path = os.path.expanduser(settings.database_path)
    settings.html_path = os.path.expanduser(settings.html_path)
    settings.label_generation_directory = os.path.expanduser(settings.label_generation_directory)


def load_settings(verify=True) -> Settings:
    global _settings
    if _settings is None:
        # Parameter necessary to keep linter from complaining
        _settings = Settings(**{})

    expand_paths(_settings)

    if verify:
        verify_settings(_settings)

    return _settings
