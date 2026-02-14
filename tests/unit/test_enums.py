"""Unit tests for enum values and edge cases."""

import pytest

from pyfuncov.models.bin import Bin
from pyfuncov.models.enums import BinKind, OutOfBoundsMode


class TestBinKindEnum:
    """Tests for BinKind enum values."""

    def test_bin_kind_discrete(self):
        """Test BinKind.DISCRETE value."""
        assert BinKind.DISCRETE.value == "discrete"

    def test_bin_kind_range(self):
        """Test BinKind.RANGE value."""
        assert BinKind.RANGE.value == "range"

    def test_bin_kind_transition(self):
        """Test BinKind.TRANSITION value."""
        assert BinKind.TRANSITION.value == "transition"

    def test_bin_kind_all_values(self):
        """Test all BinKind enum values exist."""
        values = [bk.value for bk in BinKind]
        assert "discrete" in values
        assert "range" in values
        assert "transition" in values


class TestOutOfBoundsModeEnum:
    """Tests for OutOfBoundsMode enum values."""

    def test_out_of_bounds_ignore(self):
        """Test OutOfBoundsMode.IGNORE value."""
        assert OutOfBoundsMode.IGNORE.value == "ignore"

    def test_out_of_bounds_warn(self):
        """Test OutOfBoundsMode.WARN value."""
        assert OutOfBoundsMode.WARN.value == "warn"

    def test_out_of_bounds_error(self):
        """Test OutOfBoundsMode.ERROR value."""
        assert OutOfBoundsMode.ERROR.value == "error"

    def test_out_of_bounds_all_values(self):
        """Test all OutOfBoundsMode enum values exist."""
        values = [ob.value for ob in OutOfBoundsMode]
        assert "ignore" in values
        assert "warn" in values
        assert "error" in values


class TestExtremeValues:
    """Tests for extreme values handling."""

    def test_discrete_bin_very_large_number(self):
        """Test discrete bin with very large number."""
        bin = Bin(name="large", bin_type=BinKind.DISCRETE, value=10**18)
        bin.validate()
        assert bin.match_discrete(10**18) is True
        assert bin.match_discrete(0) is False

    def test_discrete_bin_negative_number(self):
        """Test discrete bin with negative number."""
        bin = Bin(name="negative", bin_type=BinKind.DISCRETE, value=-100)
        bin.validate()
        assert bin.match_discrete(-100) is True
        assert bin.match_discrete(100) is False

    def test_range_bin_large_range(self):
        """Test range bin with large range."""
        bin = Bin(name="large_range", bin_type=BinKind.RANGE, range_min=-10**9, range_max=10**9)
        bin.validate()
        assert bin.match_range(-10**9) is True
        assert bin.match_range(0) is True
        assert bin.match_range(10**9) is True
        assert bin.match_range(10**9 + 1) is False

    def test_discrete_bin_empty_string(self):
        """Test discrete bin with empty string."""
        bin = Bin(name="empty", bin_type=BinKind.DISCRETE, value="")
        bin.validate()
        assert bin.match_discrete("") is True
        assert bin.match_discrete("test") is False

    def test_discrete_bin_string(self):
        """Test discrete bin with string value."""
        bin = Bin(name="string_val", bin_type=BinKind.DISCRETE, value="test_string")
        bin.validate()
        assert bin.match_discrete("test_string") is True
        assert bin.match_discrete("other") is False


class TestInvalidInputs:
    """Tests for invalid input handling."""

    def test_discrete_bin_with_none_value(self):
        """Test discrete bin with None value raises on validation."""
        bin = Bin(name="none_bin", bin_type=BinKind.DISCRETE, value=None)
        with pytest.raises(ValueError, match="DISCRETE bin requires a value"):
            bin.validate()

    def test_range_bin_without_bounds(self):
        """Test range bin without bounds raises on validation."""
        bin = Bin(name="no_bounds", bin_type=BinKind.RANGE)
        with pytest.raises(ValueError, match="RANGE bin requires range_min and range_max"):
            bin.validate()

    def test_transition_bin_without_values(self):
        """Test transition bin without values raises on validation."""
        bin = Bin(name="no_transition", bin_type=BinKind.TRANSITION)
        with pytest.raises(ValueError, match="TRANSITION bin requires from_value and to_value"):
            bin.validate()

    def test_transition_bin_same_values(self):
        """Test transition bin with same from/to values raises."""
        bin = Bin(name="same", bin_type=BinKind.TRANSITION, from_value=1, to_value=1)
        with pytest.raises(ValueError, match="from_value != to_value"):
            bin.validate()

    def test_range_bin_invalid_order(self):
        """Test range bin with reversed range raises."""
        bin = Bin(name="reversed", bin_type=BinKind.RANGE, range_min=100, range_max=0)
        with pytest.raises(ValueError, match="range_min must be <= range_max"):
            bin.validate()

    def test_empty_bin_name(self):
        """Test empty bin name raises on validation."""
        bin = Bin(name="", bin_type=BinKind.DISCRETE, value=1)
        with pytest.raises(ValueError, match="must be non-empty"):
            bin.validate()


class TestBinTypeValidation:
    """Tests for bin type specific validation."""

    def test_discrete_bin_with_range_params(self):
        """Test discrete bin with range params is allowed (params ignored)."""
        bin = Bin(name="discrete", bin_type=BinKind.DISCRETE, value=1, range_min=0, range_max=10)
        bin.validate()  # Should not raise
        assert bin.match_discrete(1) is True

    def test_range_bin_with_discrete_value(self):
        """Test range bin with discrete value is allowed (value ignored)."""
        bin = Bin(name="range", bin_type=BinKind.RANGE, range_min=0, range_max=10, value=5)
        bin.validate()  # Should not raise
        assert bin.match_range(5) is True

    def test_transition_bin_with_other_params(self):
        """Test transition bin with other params is allowed."""
        bin = Bin(name="transition", bin_type=BinKind.TRANSITION, from_value=0, to_value=1, value=5)
        bin.validate()  # Should not raise
        assert bin.match_transition(0, 1) is True


class TestEdgeCases:
    """Additional edge case tests."""

    def test_bin_hit_multiple_times(self):
        """Test bin can be hit multiple times."""
        bin = Bin(name="test", bin_type=BinKind.DISCRETE, value=1)
        assert bin.hits == 0

        bin.hit()
        assert bin.hits == 1

        bin.hit()
        bin.hit()
        assert bin.hits == 3

    def test_bin_last_hit_timestamp(self):
        """Test bin records last hit timestamp."""
        bin = Bin(name="test", bin_type=BinKind.DISCRETE, value=1)
        assert bin.last_hit is None

        bin.hit()
        assert bin.last_hit is not None

    def test_out_of_bounds_mode_values(self):
        """Test all out of bounds modes work correctly."""
        # Just verify they exist
        assert OutOfBoundsMode.IGNORE is not None
        assert OutOfBoundsMode.WARN is not None
        assert OutOfBoundsMode.ERROR is not None
