"""Typed application settings loaded from the environment."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for Project Alpha.

    Environment variables use the ``PROJECT_ALPHA_`` prefix. Nested application
    components receive this object through dependency injection rather than
    reading process state themselves.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="PROJECT_ALPHA_",
        extra="ignore",
    )

    app_name: str = "project-alpha"
    environment: str = "development"
    log_level: str = "INFO"
    database_path: Path = Field(default=Path("data/project_alpha.duckdb"))

    @property
    def is_production(self) -> bool:
        """Return whether the current environment is production."""
        return self.environment.casefold() == "production"
