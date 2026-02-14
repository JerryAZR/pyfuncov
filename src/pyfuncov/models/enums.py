"""Enumerations for pyfuncov domain models."""

from enum import Enum


class BinKind(Enum):
    """Kind of bin for coverage tracking.

    Attributes:
        DISCRETE: Exact value matching
        RANGE: Value within range [min, max]
        TRANSITION: Sequence matching (prev -> current)
    """

    DISCRETE = "discrete"
    RANGE = "range"
    TRANSITION = "transition"


class OutOfBoundsMode(Enum):
    """Mode for handling values outside defined bins.

    Attributes:
        IGNORE: Don't track, continue
        WARN: Log warning, continue
        ERROR: Raise exception
    """

    IGNORE = "ignore"
    WARN = "warn"
    ERROR = "error"
