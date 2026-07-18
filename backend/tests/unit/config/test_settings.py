"""Tests for typed application settings."""

from pathlib import Path

from app.core.config import Settings
from pytest import MonkeyPatch


def test_settings_loads_prefixed_environment_variables(monkeypatch: MonkeyPatch) -> None:
    """Settings should read Project Alpha's namespaced environment variables."""
    monkeypatch.setenv("PROJECT_ALPHA_DATABASE_PATH", "tmp/testing.duckdb")
    monkeypatch.setenv("PROJECT_ALPHA_ENVIRONMENT", "production")

    settings = Settings()

    assert settings.database_path == Path("tmp/testing.duckdb")
    assert settings.is_production


def test_settings_has_safe_defaults(monkeypatch: MonkeyPatch) -> None:
    """Settings should provide development-safe defaults without a dotenv file."""
    for variable in (
        "PROJECT_ALPHA_APP_NAME",
        "PROJECT_ALPHA_ENVIRONMENT",
        "PROJECT_ALPHA_LOG_LEVEL",
        "PROJECT_ALPHA_DATABASE_PATH",
    ):
        monkeypatch.delenv(variable, raising=False)

    settings = Settings(_env_file=None)

    assert settings.app_name == "project-alpha"
    assert settings.environment == "development"
    assert settings.database_path == Path("data/project_alpha.duckdb")
