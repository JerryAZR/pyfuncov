"""Integration tests for persistence."""

import json
import os
import tempfile

import pytest

from pyfuncov.models.bin import Bin
from pyfuncov.models.covergroup import Covergroup, clear_registry, get_all_covergroups
from pyfuncov.models.enums import BinKind, OutOfBoundsMode
from pyfuncov.storage import load_coverage, reset_coverage_data, save_coverage


@pytest.fixture(autouse=True)
def clean_state():
    """Clean up global state before each test."""
    clear_registry()
    reset_coverage_data()
    yield
    clear_registry()
    reset_coverage_data()


class TestPersistence:
    """Tests for coverage data persistence."""

    def test_save_and_load_coverage(self):
        """Test saving and loading coverage data."""
        # Create a covergroup with bins
        cg = Covergroup(name="test_cg", module="test_module")
        cg.add_coverpoint(
            name="test_cp",
            bins=[
                Bin(name="bin_1", bin_type=BinKind.DISCRETE, value=1),
                Bin(name="bin_2", bin_type=BinKind.DISCRETE, value=2),
            ],
            out_of_bounds=OutOfBoundsMode.IGNORE,
        )
        cg.register()

        # Sample some values
        cg.sample("test_cp", 1)
        cg.sample("test_cp", 1)
        cg.sample("test_cp", 2)

        # Save to temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            save_coverage(temp_path)

            # Verify file exists and has content
            assert os.path.exists(temp_path)

            with open(temp_path) as f:
                data = json.load(f)

            assert data["version"] == "1.0"
            assert data["total_runs"] == 1
            assert "test_module.test_cg" in data["covergroups"]

            cg_data = data["covergroups"]["test_module.test_cg"]
            bins = cg_data["coverpoints"]["test_cp"]["bins"]["bins"]

            assert bins["bin_1"]["hits"] == 2
            assert bins["bin_2"]["hits"] == 1
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_cumulative_aggregation(self):
        """Test that coverage data is aggregated across multiple saves."""
        # Create a covergroup
        cg = Covergroup(name="agg_test", module="test")
        cg.add_coverpoint(
            name="counter",
            bins=[
                Bin(name="zero", bin_type=BinKind.DISCRETE, value=0),
                Bin(name="one", bin_type=BinKind.DISCRETE, value=1),
            ],
        )
        cg.register()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            # First run: sample 0
            cg.sample("counter", 0)
            save_coverage(temp_path)

            # Reload and sample more
            load_coverage(temp_path)
            cg.sample("counter", 1)
            cg.sample("counter", 1)
            save_coverage(temp_path)

            # Check cumulative hits
            with open(temp_path) as f:
                data = json.load(f)

            # Should have 2 total runs
            assert data["total_runs"] == 2

            # Hits should be aggregated
            cg_data = data["covergroups"]["test.agg_test"]
            bins = cg_data["coverpoints"]["counter"]["bins"]["bins"]

            # Hits should be cumulative: zero got 1 hit, one got 2 hits
            assert bins["zero"]["hits"] == 1
            assert bins["one"]["hits"] == 2
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_load_nonexistent_file(self):
        """Test that loading nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_coverage("/nonexistent/path/coverage.json")

    def test_module_namespacing(self):
        """Test that covergroups from different modules are namespaced separately."""
        # Create covergroups in different modules with same name
        cg1 = Covergroup(name="handler", module="module_a")
        cg1.add_coverpoint("cp", bins=[Bin(name="b1", bin_type=BinKind.DISCRETE, value=1)])
        cg1.register()

        cg2 = Covergroup(name="handler", module="module_b")
        cg2.add_coverpoint("cp", bins=[Bin(name="b2", bin_type=BinKind.DISCRETE, value=2)])
        cg2.register()

        # Verify both are registered with different keys
        all_groups = get_all_covergroups()
        assert "module_a.handler" in all_groups
        assert "module_b.handler" in all_groups
        assert len(all_groups) == 2
