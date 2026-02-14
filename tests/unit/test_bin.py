"""Unit tests for Bin model."""

import pytest

from pyfuncov.models.bin import Bin
from pyfuncov.models.enums import BinKind


class TestBinDiscrete:
    """Tests for discrete bin matching."""

    def test_match_discrete_exact_value(self):
        """Test discrete bin matches exact value."""
        bin = Bin(name="type_0", bin_type=BinKind.DISCRETE, value=0)
        assert bin.match_discrete(0) is True
        assert bin.match_discrete(1) is False

    def test_match_discrete_string_value(self):
        """Test discrete bin matches string value."""
        bin = Bin(name="type_data", bin_type=BinKind.DISCRETE, value="data")
        assert bin.match_discrete("data") is True
        assert bin.match_discrete("control") is False

    def test_match_discrete_wrong_type(self):
        """Test discrete bin returns False for non-discrete bin."""
        bin = Bin(name="range_bin", bin_type=BinKind.RANGE, range_min=0, range_max=10)
        assert bin.match_discrete(5) is False


class TestBinRange:
    """Tests for range bin matching."""

    def test_match_range_within_bounds(self):
        """Test range bin matches value within range."""
        bin = Bin(name="range_0_100", bin_type=BinKind.RANGE, range_min=0, range_max=100)
        assert bin.match_range(0) is True
        assert bin.match_range(50) is True
        assert bin.match_range(100) is True

    def test_match_range_outside_bounds(self):
        """Test range bin does not match value outside range."""
        bin = Bin(name="range_0_100", bin_type=BinKind.RANGE, range_min=0, range_max=100)
        assert bin.match_range(-1) is False
        assert bin.match_range(101) is False

    def test_match_range_wrong_type(self):
        """Test range bin returns False for non-range bin."""
        bin = Bin(name="discrete_bin", bin_type=BinKind.DISCRETE, value=5)
        assert bin.match_range(5) is False


class TestBinTransition:
    """Tests for transition bin matching."""

    def test_match_transition_exact(self):
        """Test transition bin matches exact transition."""
        bin = Bin(name="idle_to_active", bin_type=BinKind.TRANSITION, from_value=0, to_value=1)
        assert bin.match_transition(0, 1) is True
        assert bin.match_transition(1, 0) is False

    def test_match_transition_reverse(self):
        """Test transition bin does not match reverse transition."""
        bin = Bin(name="active_to_idle", bin_type=BinKind.TRANSITION, from_value=1, to_value=0)
        assert bin.match_transition(1, 0) is True
        assert bin.match_transition(0, 1) is False


class TestBinHit:
    """Tests for bin hit tracking."""

    def test_hit_increments_count(self):
        """Test hitting a bin increments the hit count."""
        bin = Bin(name="test", bin_type=BinKind.DISCRETE, value=1)
        assert bin.hits == 0
        bin.hit()
        assert bin.hits == 1
        bin.hit()
        assert bin.hits == 2

    def test_hit_records_timestamp(self):
        """Test hitting a bin records last_hit timestamp."""
        bin = Bin(name="test", bin_type=BinKind.DISCRETE, value=1)
        assert bin.last_hit is None
        bin.hit()
        assert bin.last_hit is not None


class TestBinValidation:
    """Tests for bin validation."""

    def test_validate_discrete_ok(self):
        """Test discrete bin validation passes with value."""
        bin = Bin(name="test", bin_type=BinKind.DISCRETE, value=1)
        bin.validate()  # Should not raise

    def test_validate_discrete_missing_value(self):
        """Test discrete bin validation fails without value."""
        bin = Bin(name="test", bin_type=BinKind.DISCRETE)
        with pytest.raises(ValueError, match="DISCRETE bin requires a value"):
            bin.validate()

    def test_validate_range_ok(self):
        """Test range bin validation passes with valid range."""
        bin = Bin(name="test", bin_type=BinKind.RANGE, range_min=0, range_max=100)
        bin.validate()  # Should not raise

    def test_validate_range_missing_bounds(self):
        """Test range bin validation fails without bounds."""
        bin = Bin(name="test", bin_type=BinKind.RANGE)
        with pytest.raises(ValueError, match="RANGE bin requires range_min and range_max"):
            bin.validate()

    def test_validate_range_invalid_order(self):
        """Test range bin validation fails with reversed range."""
        bin = Bin(name="test", bin_type=BinKind.RANGE, range_min=100, range_max=0)
        with pytest.raises(ValueError, match="range_min must be <= range_max"):
            bin.validate()

    def test_validate_transition_ok(self):
        """Test transition bin validation passes with valid transition."""
        bin = Bin(name="test", bin_type=BinKind.TRANSITION, from_value=0, to_value=1)
        bin.validate()  # Should not raise

    def test_validate_transition_missing_values(self):
        """Test transition bin validation fails without values."""
        bin = Bin(name="test", bin_type=BinKind.TRANSITION)
        with pytest.raises(ValueError, match="TRANSITION bin requires from_value and to_value"):
            bin.validate()

    def test_validate_transition_same_values(self):
        """Test transition bin validation fails with same values."""
        bin = Bin(name="test", bin_type=BinKind.TRANSITION, from_value=1, to_value=1)
        with pytest.raises(ValueError, match="from_value != to_value"):
            bin.validate()

    def test_validate_empty_name(self):
        """Test validation fails with empty name."""
        bin = Bin(name="", bin_type=BinKind.DISCRETE, value=1)
        with pytest.raises(ValueError, match="must be non-empty"):
            bin.validate()
