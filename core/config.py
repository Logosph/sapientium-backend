from functools import lru_cache
from urllib.parse import quote_plus

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    mongo_host: str = Field(default="localhost")
    mongo_port: int = Field(default=27017, ge=1, le=65535)
    mongo_user: str = Field(default="")
    mongo_password: str = Field(default="")
    mongo_db: str = Field(default="")
    mongo_auth_source: str = Field(default="")

    @property
    def mongodb_uri(self) -> str:
        u = quote_plus(self.mongo_user)
        p = quote_plus(self.mongo_password)
        a = quote_plus(self.mongo_auth_source)
        return (
            f"mongodb://"
            f"{f'{u}:{p}@' if self.mongo_user else ''}"
            f"{self.mongo_host}:{self.mongo_port}"
            f"{f'/{self.mongo_db}' if self.mongo_db else ''}"
            f"{f'?authSource={a}' if self.mongo_auth_source else ''}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
