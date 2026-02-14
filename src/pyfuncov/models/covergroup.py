"""Covergroup dataclass for pyfuncov domain models."""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from pyfuncov.models.bin import Bin
from pyfuncov.models.coverpoint import Coverpoint
from pyfuncov.models.enums import OutOfBoundsMode

logger = logging.getLogger(__name__)

# Global registry for covergroups
_covergroup_registry: Dict[str, "Covergroup"] = {}


@dataclass
class Covergroup:
    """A named container for related coverage points that defines a coverage domain.

    Attributes:
        name: Unique identifier for the covergroup
        coverpoints: List of coverpoints in this group
        module: Module path (for namespace collision resolution)
        created_at: Creation timestamp
        _prev_values: Internal state for transition tracking
    """

    name: str
    coverpoints: List[Coverpoint] = field(default_factory=list)
    module: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    _prev_values: Dict[str, int] = field(default_factory=dict, repr=False)

    def add_coverpoint(self, name: str, bins: List[Bin], out_of_bounds: OutOfBoundsMode = OutOfBoundsMode.IGNORE) -> Coverpoint:
        """Add a coverpoint with bins to this covergroup.

        Args:
            name: Name of the coverpoint
            bins: List of bins for this coverpoint
            out_of_bounds: How to handle values outside bins

        Returns:
            The created Coverpoint
        """
        coverpoint = Coverpoint(name=name, bins=bins, out_of_bounds=out_of_bounds)
        self.coverpoints.append(coverpoint)
        return coverpoint

    def sample(self, coverpoint_name: str, value: Any) -> Optional[Bin]:
        """Sample a value against a coverpoint.

        Args:
            coverpoint_name: Name of the coverpoint to sample against
            value: The value to sample

        Returns:
            The bin that was hit, or None if no match
        """
        coverpoint = self._find_coverpoint(coverpoint_name)
        if coverpoint is None:
            logger.warning(f"Coverpoint '{coverpoint_name}' not found in covergroup '{self.name}'")
            return None

        prev_value = self._prev_values.get(coverpoint_name)
        matching_bin = coverpoint.find_matching_bin(value, prev_value)

        if matching_bin is not None:
            matching_bin.hit()
            # Update previous value for transition tracking
            if isinstance(value, int):
                self._prev_values[coverpoint_name] = value
            return matching_bin

        # Handle out-of-bounds
        if coverpoint.out_of_bounds == OutOfBoundsMode.ERROR:
            raise ValueError(f"Value {value} is out of bounds for coverpoint '{coverpoint_name}'")
        elif coverpoint.out_of_bounds == OutOfBoundsMode.WARN:
            logger.warning(f"Value {value} is out of bounds for coverpoint '{coverpoint_name}'")

        return None

    def register(self, module: Optional[str] = None) -> None:
        """Register this covergroup globally.

        Args:
            module: Module path for namespacing (auto-detected if not provided)
        """
        if module:
            self.module = module

        # Create namespaced key
        key = f"{self.module}.{self.name}" if self.module else self.name

        if key in _covergroup_registry:
            logger.warning(f"Covergroup '{key}' already registered, overwriting")

        _covergroup_registry[key] = self

    def _find_coverpoint(self, name: str) -> Optional[Coverpoint]:
        """Find a coverpoint by name.

        Args:
            name: Name of the coverpoint

        Returns:
            The Coverpoint, or None if not found
        """
        for cp in self.coverpoints:
            if cp.name == name:
                return cp
        return None

    def to_dict(self) -> Dict:
        """Serialize covergroup to dictionary for JSON storage.

        Returns:
            Dictionary representation of the covergroup
        """
        return {
            "name": self.name,
            "module": self.module,
            "created_at": self.created_at.isoformat(),
            "coverpoints": {
                cp.name: {
                    "name": cp.name,
                    "bins": {
                        "bins": {
                            bin.name: {
                                "name": bin.name,
                                "bin_type": bin.bin_type.value,
                                "value": bin.value,
                                "range_min": bin.range_min,
                                "range_max": bin.range_max,
                                "from_value": bin.from_value,
                                "to_value": bin.to_value,
                                "hits": bin.hits,
                                "last_hit": bin.last_hit.isoformat() if bin.last_hit else None,
                            }
                            for bin in cp.bins
                        }
                    },
                    "out_of_bounds": cp.out_of_bounds.value,
                }
                for cp in self.coverpoints
            },
        }


def get_covergroup(name: str, module: str = "") -> Optional[Covergroup]:
    """Get a registered covergroup by name.

    Args:
        name: Name of the covergroup
        module: Module path for namespacing

    Returns:
        The Covergroup, or None if not found
    """
    key = f"{module}.{name}" if module else name
    return _covergroup_registry.get(key)


def get_all_covergroups() -> Dict[str, Covergroup]:
    """Get all registered covergroups.

    Returns:
        Dictionary of all registered covergroups
    """
    return _covergroup_registry.copy()


def clear_registry() -> None:
    """Clear all registered covergroups. Useful for testing."""
    _covergroup_registry.clear()
