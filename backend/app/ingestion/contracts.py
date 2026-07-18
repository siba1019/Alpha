"""Contracts for bringing market data into the application boundary."""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True, slots=True)
class IngestionResult:
    """Outcome metadata returned by a data-ingestion operation."""

    source: str
    records_received: int
    completed_at: datetime


class DataIngestionPort(Protocol):
    """Application boundary for a market-data ingestion provider."""

    def fetch(self, symbols: Iterable[str]) -> IngestionResult:
        """Fetch data for the requested symbols without prescribing its source."""
