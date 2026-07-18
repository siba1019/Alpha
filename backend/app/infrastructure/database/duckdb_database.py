"""DuckDB connection lifecycle management."""

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import duckdb
from duckdb import DuckDBPyConnection

from app.core.logging.setup import get_logger

logger = get_logger(__name__)


class DuckDBDatabase:
    """Create short-lived DuckDB connections for an injected database location."""

    def __init__(self, database_path: Path) -> None:
        """Initialize the adapter with a persistent DuckDB file path."""
        self._database_path = database_path

    @property
    def database_path(self) -> Path:
        """Return the configured database file path."""
        return self._database_path

    def initialize(self) -> None:
        """Ensure the database's parent directory and file can be created."""
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection():
            pass
        logger.info("database_initialized", database_path=str(self._database_path))

    @contextmanager
    def connection(self) -> Iterator[DuckDBPyConnection]:
        """Yield a connection and close it deterministically when work completes."""
        connection = duckdb.connect(str(self._database_path))
        try:
            yield connection
        finally:
            connection.close()
