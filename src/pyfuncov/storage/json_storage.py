"""JSON storage for coverage data."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from pyfuncov.models.coverage_data import CoverageData

logger = logging.getLogger(__name__)


def _serialize_datetime(obj: Any) -> str:
    """Serialize datetime objects to ISO format."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def save_coverage_to_file(coverage_data: CoverageData, filepath: str) -> None:
    """Save coverage data to a JSON file.

    Args:
        coverage_data: The coverage data to save
        filepath: Path to the output JSON file
    """
    data = {
        "version": coverage_data.version,
        "total_runs": coverage_data.total_runs,
        "last_updated": coverage_data.last_updated.isoformat(),
        "covergroups": coverage_data.covergroups,
    }

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=_serialize_datetime)

    logger.info(f"Saved coverage data to {filepath}")


def load_coverage_from_file(filepath: str) -> CoverageData:
    """Load coverage data from a JSON file.

    Args:
        filepath: Path to the JSON file

    Returns:
        The loaded CoverageData

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"Coverage file not found: {filepath}")

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse JSON from {filepath}: {e}")
        # Return empty coverage data on parse error
        return CoverageData()

    coverage_data = CoverageData()

    # Extract version
    coverage_data.version = data.get("version", "1.0")

    # Extract total runs
    coverage_data.total_runs = data.get("total_runs", 0)

    # Extract last_updated
    last_updated_str = data.get("last_updated")
    if last_updated_str:
        try:
            coverage_data.last_updated = datetime.fromisoformat(last_updated_str)
        except (ValueError, TypeError):
            logger.warning(f"Invalid timestamp in {filepath}: {last_updated_str}")
            coverage_data.last_updated = datetime.now()

    # Extract covergroups
    coverage_data.covergroups = data.get("covergroups", {})

    logger.info(f"Loaded coverage data from {filepath}")
    return coverage_data


def merge_coverage_data(existing: CoverageData, new: CoverageData) -> CoverageData:
    """Merge new coverage data into existing data (cumulative aggregation).

    Args:
        existing: Existing coverage data
        new: New coverage data to merge

    Returns:
        Merged CoverageData
    """
    merged = CoverageData()
    merged.version = existing.version
    merged.total_runs = existing.total_runs + new.total_runs
    merged.last_updated = datetime.now()

    # Start with existing data
    merged.covergroups = dict(existing.covergroups)

    # Merge new data
    for name, cg_data in new.covergroups.items():
        if name in merged.covergroups:
            # Merge covergroups
            existing_cg = merged.covergroups[name]
            new_cg = cg_data

            # Merge coverpoints
            for cp_name, cp_data in new_cg.get("coverpoints", {}).items():
                if "coverpoints" not in existing_cg:
                    existing_cg["coverpoints"] = {}

                if cp_name in existing_cg["coverpoints"]:
                    # Merge bins - add hits
                    existing_cp = existing_cg["coverpoints"][cp_name]
                    for bin_name, bin_data in cp_data.get("bins", {}).get("bins", {}).items():
                        if bin_name in existing_cp.get("bins", {}).get("bins", {}):
                            existing_bins = existing_cp["bins"]["bins"]
                            if "hits" in bin_data and "hits" in existing_bins[bin_name]:
                                existing_bins[bin_name]["hits"] += bin_data.get("hits", 0)
                        else:
                            if "bins" not in existing_cp:
                                existing_cp["bins"] = {"bins": {}}
                            existing_cp["bins"]["bins"][bin_name] = bin_data
                else:
                    existing_cg["coverpoints"][cp_name] = cp_data
        else:
            # Add new covergroup
            merged.covergroups[name] = cg_data

    return merged
