"""Tests for structured logging configuration."""

from app.core.logging.setup import configure_logging, get_logger
from pytest import CaptureFixture


def test_configure_logging_emits_json(capsys: CaptureFixture[str]) -> None:
    """Configured loggers should emit structured JSON to standard output."""
    configure_logging("INFO")

    get_logger("test.logger").info("database_initialized", database="research")

    output = capsys.readouterr().out
    assert '"event": "database_initialized"' in output
    assert '"database": "research"' in output
    assert '"level": "info"' in output
