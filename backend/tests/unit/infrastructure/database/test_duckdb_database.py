"""Tests for the DuckDB adapter."""

from pathlib import Path

from app.infrastructure.database import DuckDBDatabase


def test_initialize_creates_database_file(tmp_path: Path) -> None:
    """Initialization should create a database and missing parent directories."""
    database_path = tmp_path / "nested" / "research.duckdb"
    database = DuckDBDatabase(database_path)

    database.initialize()

    assert database_path.is_file()


def test_connection_can_execute_sql(tmp_path: Path) -> None:
    """The database adapter should yield a functioning DuckDB connection."""
    database = DuckDBDatabase(tmp_path / "research.duckdb")
    database.initialize()

    with database.connection() as connection:
        result = connection.execute("SELECT 42").fetchone()

    assert result == (42,)


def test_database_path_returns_configured_path(tmp_path: Path) -> None:
    """The adapter should expose the path it was configured to manage."""
    database_path = tmp_path / "research.duckdb"

    database = DuckDBDatabase(database_path)

    assert database.database_path == database_path
