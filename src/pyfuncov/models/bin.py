"""Bin dataclass for pyfuncov domain models."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from pyfuncov.models.enums import BinKind


@dataclass
class Bin:
    """A discrete condition within a coverpoint that tracks a specific value, range, or transition.

    Attributes:
        name: Human-readable name for the bin
        bin_type: Kind of bin (DISCRETE, RANGE, TRANSITION)
        value: For DISCRETE bins - the exact value to match
        range_min: For RANGE bins - minimum value (inclusive)
        range_max: For RANGE bins - maximum value (inclusive)
        from_value: For TRANSITION bins - starting value
        to_value: For TRANSITION bins - ending value
        hits: Number of times this bin was hit
        last_hit: Last hit timestamp
    """

    name: str
    bin_type: BinKind
    value: Optional[Any] = None
    range_min: Optional[int] = None
    range_max: Optional[int] = None
    from_value: Optional[int] = None
    to_value: Optional[int] = None
    hits: int = 0
    last_hit: Optional[datetime] = None

    def match_discrete(self, value: Any) -> bool:
        """Check if value matches this discrete bin.

        Args:
            value: The value to check

        Returns:
            True if value matches the bin's exact value
        """
        if self.bin_type != BinKind.DISCRETE:
            return False
        return self.value == value

    def match_range(self, value: int) -> bool:
        """Check if value falls within this range bin.

        Args:
            value: The integer value to check

        Returns:
            True if value is within [range_min, range_max]
        """
        if self.bin_type != BinKind.RANGE:
            return False
        if self.range_min is None or self.range_max is None:
            return False
        return self.range_min <= value <= self.range_max

    def match_transition(self, from_val: int, to_val: int) -> bool:
        """Check if this is a matching transition.

        Args:
            from_val: The previous value
            to_val: The current value

        Returns:
            True if transition matches from_value -> to_value
        """
        if self.bin_type != BinKind.TRANSITION:
            return False
        if self.from_value is None or self.to_value is None:
            return False
        return self.from_value == from_val and self.to_value == to_val

    def hit(self) -> None:
        """Record a hit on this bin."""
        self.hits += 1
        self.last_hit = datetime.now()

    def validate(self) -> None:
        """Validate bin definition per data-model.md.

        Raises:
            ValueError: If validation fails
        """
        if not self.name or not self.name.strip():
            raise ValueError("Bin name must be non-empty")

        if self.bin_type == BinKind.DISCRETE:
            if self.value is None:
                raise ValueError(f"Bin '{self.name}': DISCRETE bin requires a value")
        elif self.bin_type == BinKind.RANGE:
            if self.range_min is None or self.range_max is None:
                raise ValueError(f"Bin '{self.name}': RANGE bin requires range_min and range_max")
            if self.range_min > self.range_max:
                raise ValueError(f"Bin '{self.name}': range_min must be <= range_max")
        elif self.bin_type == BinKind.TRANSITION:
            if self.from_value is None or self.to_value is None:
                raise ValueError(f"Bin '{self.name}': TRANSITION bin requires from_value and to_value")
            if self.from_value == self.to_value:
                raise ValueError(f"Bin '{self.name}': TRANSITION bin requires from_value != to_value")
