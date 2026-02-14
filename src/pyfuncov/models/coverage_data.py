"""CoverageData dataclass for pyfuncov domain models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict


@dataclass
class CoverageData:
    """The accumulated hits across all bins from one or more test runs.

    Attributes:
        covergroups: Map of covergroup name to data
        total_runs: Number of test runs aggregated
        last_updated: Last update timestamp
        version: Format version for compatibility
    """

    covergroups: Dict[str, Dict] = field(default_factory=dict)
    total_runs: int = 0
    last_updated: datetime = field(default_factory=datetime.now)
    version: str = "1.0"
