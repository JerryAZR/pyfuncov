"""Unit tests for Covergroup model."""

import pytest

from pyfuncov.models.bin import Bin
from pyfuncov.models.covergroup import (
    Covergroup,
    clear_registry,
    get_all_covergroups,
    get_covergroup,
)
from pyfuncov.models.coverpoint import Coverpoint
from pyfuncov.models.enums import BinKind, OutOfBoundsMode


class TestCovergroupCreation:
    """Tests for Covergroup creation."""

    def test_create_covergroup_basic(self):
        """Test creating a covergroup with basic parameters."""
        cg = Covergroup(name="test_cg")
        assert cg.name == "test_cg"
        assert cg.coverpoints == []
        assert cg.module == ""
        assert cg.created_at is not None

    def test_create_covergroup_with_module(self):
        """Test creating a covergroup with module namespace."""
        cg = Covergroup(name="test_cg", module="myapp.tests")
        assert cg.name == "test_cg"
        assert cg.module == "myapp.tests"

    def test_create_covergroup_with_coverpoints(self):
        """Test creating a covergroup with pre-defined coverpoints."""
        cp1 = Coverpoint(name="cp1", bins=[])
        cp2 = Coverpoint(name="cp2", bins=[])
        cg = Covergroup(name="test_cg", coverpoints=[cp1, cp2])
        assert len(cg.coverpoints) == 2
        assert cg.coverpoints[0].name == "cp1"
        assert cg.coverpoints[1].name == "cp2"


class TestCovergroupAddCoverpoint:
    """Tests for adding coverpoints to covergroup."""

    def test_add_coverpoint(self):
        """Test adding a coverpoint to a covergroup."""
        cg = Covergroup(name="test_cg")
        bins = [Bin(name="bin1", bin_type=BinKind.DISCRETE, value=1)]
        cp = cg.add_coverpoint("cp1", bins)
        assert cp.name == "cp1"
        assert len(cg.coverpoints) == 1
        assert cp.bins[0].name == "bin1"

    def test_add_coverpoint_with_out_of_bounds(self):
        """Test adding a coverpoint with out of bounds mode."""
        cg = Covergroup(name="test_cg")
        bins = [Bin(name="bin1", bin_type=BinKind.DISCRETE, value=1)]
        cp = cg.add_coverpoint("cp1", bins, out_of_bounds=OutOfBoundsMode.ERROR)
        assert cp.out_of_bounds == OutOfBoundsMode.ERROR


class TestCovergroupRegistration:
    """Tests for covergroup registration."""

    def setup_method(self):
        """Clear registry before each test."""
        clear_registry()

    def test_register_covergroup(self):
        """Test registering a covergroup."""
        cg = Covergroup(name="test_cg")
        cg.register()
        assert get_covergroup("test_cg") is cg

    def test_register_covergroup_with_module(self):
        """Test registering a covergroup with module namespace."""
        cg = Covergroup(name="test_cg", module="myapp")
        cg.register()
        assert get_covergroup("test_cg", module="myapp") is cg

    def test_register_covergroup_with_module_param(self):
        """Test registering a covergroup and passing module as parameter."""
        cg = Covergroup(name="test_cg")
        cg.register(module="mymodule")
        assert get_covergroup("test_cg", module="mymodule") is cg
        assert cg.module == "mymodule"

    def test_register_duplicate_covergroup(self):
        """Test registering a duplicate covergroup (should warn but succeed)."""
        cg1 = Covergroup(name="test_cg")
        cg1.register()
        cg2 = Covergroup(name="test_cg")
        cg2.register()  # Should overwrite
        assert get_covergroup("test_cg") is cg2

    def test_get_all_covergroups(self):
        """Test getting all registered covergroups."""
        cg1 = Covergroup(name="cg1")
        cg2 = Covergroup(name="cg2")
        cg1.register()
        cg2.register()
        all_cgs = get_all_covergroups()
        assert len(all_cgs) == 2
        assert "cg1" in all_cgs
        assert "cg2" in all_cgs


class TestCovergroupSample:
    """Tests for Covergroup.sample() method."""

    def setup_method(self):
        """Clear registry before each test."""
        clear_registry()

    def test_sample_discrete_bin_hit(self):
        """Test sampling a value that hits a discrete bin."""
        cg = Covergroup(name="test_cg")
        bins = [
            Bin(name="bin0", bin_type=BinKind.DISCRETE, value=0),
            Bin(name="bin1", bin_type=BinKind.DISCRETE, value=1),
        ]
        cg.add_coverpoint("cp1", bins)
        cg.register()

        result = cg.sample("cp1", 0)
        assert result is not None
        assert result.name == "bin0"
        assert result.hits == 1

    def test_sample_range_bin_hit(self):
        """Test sampling a value that hits a range bin."""
        cg = Covergroup(name="test_cg")
        bins = [Bin(name="range_bin", bin_type=BinKind.RANGE, range_min=0, range_max=10)]
        cg.add_coverpoint("cp1", bins)
        cg.register()

        result = cg.sample("cp1", 5)
        assert result is not None
        assert result.name == "range_bin"
        assert result.hits == 1

    def test_sample_no_match(self):
        """Test sampling a value that doesn't match any bin."""
        cg = Covergroup(name="test_cg")
        bins = [Bin(name="bin0", bin_type=BinKind.DISCRETE, value=0)]
        cg.add_coverpoint("cp1", bins)
        cg.register()

        result = cg.sample("cp1", 1)  # No bin for value 1
        assert result is None

    def test_sample_nonexistent_coverpoint(self):
        """Test sampling against a non-existent coverpoint."""
        cg = Covergroup(name="test_cg")
        cg.register()

        result = cg.sample("nonexistent", 0)
        assert result is None

    def test_sample_transition_bin(self):
        """Test sampling a value that hits a transition bin."""
        cg = Covergroup(name="test_cg")
        bins = [Bin(name="idle_to_active", bin_type=BinKind.TRANSITION, from_value=0, to_value=1)]
        cg.add_coverpoint("cp1", bins)
        cg.register()

        # First sample - no transition yet
        cg.sample("cp1", 0)
        # Second sample - transition from 0 to 1
        result = cg.sample("cp1", 1)
        assert result is not None
        assert result.name == "idle_to_active"
        assert result.hits == 1

    def test_sample_with_out_of_bounds_error(self):
        """Test sampling with out of bounds error mode."""
        cg = Covergroup(name="test_cg")
        bins = [Bin(name="bin0", bin_type=BinKind.DISCRETE, value=0)]
        cg.add_coverpoint("cp1", bins, out_of_bounds=OutOfBoundsMode.ERROR)
        cg.register()

        with pytest.raises(ValueError, match="out of bounds"):
            cg.sample("cp1", 99)

    def test_sample_with_out_of_bounds_warn(self):
        """Test sampling with out of bounds warn mode."""
        cg = Covergroup(name="test_cg")
        bins = [Bin(name="bin0", bin_type=BinKind.DISCRETE, value=0)]
        cg.add_coverpoint("cp1", bins, out_of_bounds=OutOfBoundsMode.WARN)
        cg.register()

        result = cg.sample("cp1", 99)  # Out of bounds
        assert result is None  # Returns None but doesn't raise

    def test_sample_multiple_hits(self):
        """Test multiple samples increment hit count."""
        cg = Covergroup(name="test_cg")
        bins = [Bin(name="bin0", bin_type=BinKind.DISCRETE, value=0)]
        cg.add_coverpoint("cp1", bins)
        cg.register()

        cg.sample("cp1", 0)
        cg.sample("cp1", 0)
        cg.sample("cp1", 0)

        assert cg.coverpoints[0].bins[0].hits == 3


class TestCovergroupSerialization:
    """Tests for Covergroup.to_dict() method."""

    def test_to_dict_basic(self):
        """Test serializing a basic covergroup."""
        cg = Covergroup(name="test_cg")
        bins = [Bin(name="bin0", bin_type=BinKind.DISCRETE, value=0)]
        cg.add_coverpoint("cp1", bins)

        result = cg.to_dict()
        assert result["name"] == "test_cg"
        assert result["module"] == ""
        assert "created_at" in result
        assert "coverpoints" in result

    def test_to_dict_with_coverpoints(self):
        """Test serializing covergroup with coverpoints and bins."""
        cg = Covergroup(name="test_cg", module="myapp")
        bins = [
            Bin(name="bin0", bin_type=BinKind.DISCRETE, value=0),
            Bin(name="range_bin", bin_type=BinKind.RANGE, range_min=0, range_max=10),
        ]
        cg.add_coverpoint("cp1", bins)

        result = cg.to_dict()
        assert result["module"] == "myapp"
        assert "cp1" in result["coverpoints"]

    def test_to_dict_with_hits(self):
        """Test serializing covergroup with bin hits."""
        cg = Covergroup(name="test_cg")
        bins = [Bin(name="bin0", bin_type=BinKind.DISCRETE, value=0)]
        cg.add_coverpoint("cp1", bins)
        cg.sample("cp1", 0)  # Hit the bin

        result = cg.to_dict()
        cp_data = result["coverpoints"]["cp1"]
        bin_data = cp_data["bins"]["bins"]["bin0"]
        assert bin_data["hits"] == 1
        assert bin_data["last_hit"] is not None
