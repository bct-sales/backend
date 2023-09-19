import logging
from typing import Optional
import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict
import sys


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='BCT_', env_file='.env', env_file_encoding='utf-8')

    database_path: Optional[str] = None

    jwt_secret_key: str = ""

    jwt_algorithm: str = 'HS256'

    jwt_expiration: int = 6 * 60 # 6 Hours

    label_generation_directory: str = 'g:/temp'

    @pydantic.computed_field # type: ignore[misc]
    @property
    def database_url(self) -> str:
        if self.database_path:
            return f'sqlite:///{self.database_path}'
        else:
            return 'sqlite:///'


_settings: Optional[Settings] = None


def load_settings() -> Settings:
    global _settings
    if _settings is None:
        # Parameter necessary to keep linter from complaining
        _settings = Settings(**{})
    if len(_settings.jwt_secret_key) == 0:
        logging.critical("No JWT key found!")
        raise RuntimeError("No JWT key found")
    return _settings
