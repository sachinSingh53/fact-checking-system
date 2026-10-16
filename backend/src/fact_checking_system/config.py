from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="FCS_",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Fact Checking System"
    environment: Literal["local", "test", "staging", "production"] = "local"
    log_level: str = "INFO"
    database_url: str = Field(
        default="postgresql+psycopg://fact_checker:fact_checker@localhost:5432/fact_checker"
    )
    temporal_host: str = "localhost:7233"
    temporal_namespace: str = "default"
    temporal_task_queue: str = "fact-checking"


@lru_cache
def get_settings() -> Settings:
    return Settings()
