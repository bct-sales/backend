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

    qr_directory: str = ''

    @pydantic.computed_field # type: ignore[misc]
    @property
    def database_url(self) -> str:
        if self.database_path:
            return f'sqlite:///{self.database_path}'
        else:
            return 'sqlite:///'


_settings: Optional[Settings] = None


def verify_settings(settings: Settings) -> None:
    def abort(message):
        logging.critical(message)
        raise RuntimeError(message)

    if len(settings.jwt_secret_key) == 0:
        abort("No JWT key found! Set BCT_JWT_SECRET_KEY")
    if len(settings.html_path) == 0:
        abort("No HTML path set! Set BCT_HTML_PATH")
    if not os.path.isfile(settings.html_path):
        abort(f"No HTML found at {settings.html_path}!")
    if len(settings.label_generation_directory) == 0:
        abort("No label generation directory set! Set BCT_BCT_LABEL_GENERATION_DIRECTORY")
    if not os.path.isdir(settings.label_generation_directory):
        abort(f"Label generation directory {settings.label_generation_directory} does not exist!")
    if len(settings.qr_directory) == 0:
        abort("No qr_directory set! Set BCT_QR_DIRECTORY")
    if not os.path.isdir(settings.qr_directory):
        abort(f"qr_path {settings.qr_directory} does not exist!")


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
