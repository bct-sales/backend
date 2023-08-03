from typing import Optional
import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='BCT_')

    database_path: str

    @pydantic.computed_field
    @property
    def database_url(self) -> str:
        return f'sqlite:///{self.database_path}'


_settings: Optional[Settings] = None


def load_settings() -> Settings:
    global _settings
    if _settings is None:
        # Parameter necessary to keep linter from complaining
        _settings = Settings(**{})
    return _settings
