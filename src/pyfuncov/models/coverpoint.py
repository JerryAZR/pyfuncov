"""Coverpoint dataclass for pyfuncov domain models."""

from dataclasses import dataclass, field
from typing import Any, List, Optional

from pyfuncov.models.bin import Bin
from pyfuncov.models.enums import OutOfBoundsMode


@dataclass
class Coverpoint:
    """A specific point within a covergroup where coverage is measured.

    Attributes:
        name: Unique identifier within covergroup
        bins: List of bins for this coverpoint
        out_of_bounds: How to handle values outside bins
    """

    name: str
    bins: List[Bin] = field(default_factory=list)
    out_of_bounds: OutOfBoundsMode = OutOfBoundsMode.IGNORE

    def find_matching_bin(self, value: Any, prev_value: Optional[int] = None) -> Optional[Bin]:
        """Find the bin that matches the given value.

        Args:
            value: The value to match against bins
            prev_value: Previous value for transition matching

        Returns:
            The matching Bin, or None if no match
        """
        for bin in self.bins:
            if bin.match_discrete(value):
                return bin
            if bin.match_range(value):
                return bin
            if prev_value is not None and isinstance(value, int) and bin.match_transition(prev_value, value):
                return bin
        return None
