from typing import Optional
import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='BCT_')

    database_path: Optional[str] = None

    jwt_secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

    jwt_algorithm: str = 'HS256'

    jwt_expiration: int = 6 * 60 # 6 Hours

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
    return _settings
