"""Storage package for pyfuncov."""

import os
from datetime import datetime

from pyfuncov.models.coverage_data import CoverageData
from pyfuncov.models.covergroup import get_all_covergroups
from pyfuncov.storage.json_storage import (
    load_coverage_from_file,
    merge_coverage_data,
    save_coverage_to_file,
)

# Global coverage data instance
_coverage_data = CoverageData()


def save_coverage(filepath: str) -> None:
    """Save coverage data to a JSON file.

    Args:
        filepath: Path to the output JSON file
    """
    global _coverage_data

    # Check existing file to get current run count
    existing_runs = 0
    if os.path.exists(filepath):
        try:
            existing = load_coverage_from_file(filepath)
            existing_runs = existing.total_runs
        except Exception:
            pass  # If can't load, start fresh

    # Collect coverage data from all registered covergroups
    _coverage_data.total_runs = existing_runs + 1
    _coverage_data.last_updated = datetime.now()
    _coverage_data.covergroups = {}

    for key, cg in get_all_covergroups().items():
        _coverage_data.covergroups[key] = cg.to_dict()

    save_coverage_to_file(_coverage_data, filepath)


def load_coverage(filepath: str) -> None:
    """Load coverage data from a JSON file and merge with existing data.

    Args:
        filepath: Path to the JSON file
    """
    global _coverage_data

    loaded = load_coverage_from_file(filepath)
    if _coverage_data.covergroups:
        _coverage_data = merge_coverage_data(_coverage_data, loaded)
    else:
        _coverage_data = loaded


def get_coverage_data() -> CoverageData:
    """Get the current coverage data.

    Returns:
        The current CoverageData instance
    """
    return _coverage_data


def reset_coverage_data() -> None:
    """Reset the global coverage data."""
    global _coverage_data
    _coverage_data = CoverageData()
