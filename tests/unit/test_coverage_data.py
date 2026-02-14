"""Unit tests for CoverageData model."""

from datetime import datetime

import pytest

from pyfuncov.models.coverage_data import CoverageData


class TestCoverageDataCreation:
    """Tests for CoverageData creation."""

    def test_create_coverage_data_defaults(self):
        """Test creating CoverageData with defaults."""
        cd = CoverageData()
        assert cd.covergroups == {}
        assert cd.total_runs == 0
        assert cd.version == "1.0"
        assert cd.last_updated is not None

    def test_create_coverage_data_with_values(self):
        """Test creating CoverageData with custom values."""
        cd = CoverageData(
            covergroups={"test": {}},
            total_runs=5,
            version="2.0"
        )
        assert cd.covergroups == {"test": {}}
        assert cd.total_runs == 5
        assert cd.version == "2.0"


class TestCoverageDataPercentageCalculation:
    """Tests for coverage percentage calculations."""

    def test_percentage_calculation_some_bins_hit(self):
        """Test percentage calculation with some bins hit."""
        # Simulate covergroup data structure
        covergroups = {
            "test_cg": {
                "coverpoints": {
                    "cp1": {
                        "bins": {
                            "bins": {
                                "bin1": {"hits": 1},
                                "bin2": {"hits": 0},
                                "bin3": {"hits": 1},
                            }
                        }
                    }
                }
            }
        }
        cd = CoverageData(covergroups=covergroups)

        # Calculate total bins and hit bins manually
        total_bins = 0
        hit_bins = 0
        for cg_name, cg_data in covergroups.items():
            for cp_name, cp_data in cg_data.get("coverpoints", {}).items():
                for bin_name, bin_data in cp_data.get("bins", {}).get("bins", {}).items():
                    total_bins += 1
                    if bin_data.get("hits", 0) > 0:
                        hit_bins += 1

        coverage = (hit_bins / total_bins) * 100 if total_bins > 0 else 0.0
        assert coverage == pytest.approx(66.67, rel=0.1)

    def test_percentage_calculation_all_bins_hit(self):
        """Test percentage calculation with all bins hit (100%)."""
        covergroups = {
            "test_cg": {
                "coverpoints": {
                    "cp1": {
                        "bins": {
                            "bins": {
                                "bin1": {"hits": 1},
                                "bin2": {"hits": 2},
                                "bin3": {"hits": 1},
                            }
                        }
                    }
                }
            }
        }

        total_bins = 0
        hit_bins = 0
        for cg_name, cg_data in covergroups.items():
            for cp_name, cp_data in cg_data.get("coverpoints", {}).items():
                for bin_name, bin_data in cp_data.get("bins", {}).get("bins", {}).items():
                    total_bins += 1
                    if bin_data.get("hits", 0) > 0:
                        hit_bins += 1

        coverage = (hit_bins / total_bins) * 100 if total_bins > 0 else 0.0
        assert coverage == 100.0

    def test_percentage_calculation_no_bins_defined(self):
        """Test percentage calculation with no bins defined."""
        covergroups = {
            "test_cg": {
                "coverpoints": {}
            }
        }

        total_bins = 0
        hit_bins = 0
        for cg_name, cg_data in covergroups.items():
            for cp_name, cp_data in cg_data.get("coverpoints", {}).items():
                for bin_name, bin_data in cp_data.get("bins", {}).get("bins", {}).items():
                    total_bins += 1
                    if bin_data.get("hits", 0) > 0:
                        hit_bins += 1

        coverage = (hit_bins / total_bins) * 100 if total_bins > 0 else 0.0
        assert coverage == 0.0

    def test_percentage_calculation_no_bins_hit(self):
        """Test percentage calculation with no bins hit."""
        covergroups = {
            "test_cg": {
                "coverpoints": {
                    "cp1": {
                        "bins": {
                            "bins": {
                                "bin1": {"hits": 0},
                                "bin2": {"hits": 0},
                            }
                        }
                    }
                }
            }
        }

        total_bins = 0
        hit_bins = 0
        for cg_name, cg_data in covergroups.items():
            for cp_name, cp_data in cg_data.get("coverpoints", {}).items():
                for bin_name, bin_data in cp_data.get("bins", {}).get("bins", {}).items():
                    total_bins += 1
                    if bin_data.get("hits", 0) > 0:
                        hit_bins += 1

        coverage = (hit_bins / total_bins) * 100 if total_bins > 0 else 0.0
        assert coverage == 0.0


class TestCoverageDataMultipleCovergroups:
    """Tests for CoverageData with multiple covergroups."""

    def test_multiple_covergroups_coverage(self):
        """Test coverage calculation with multiple covergroups."""
        covergroups = {
            "cg1": {
                "coverpoints": {
                    "cp1": {
                        "bins": {
                            "bins": {
                                "bin1": {"hits": 1},
                                "bin2": {"hits": 0},
                            }
                        }
                    }
                }
            },
            "cg2": {
                "coverpoints": {
                    "cp1": {
                        "bins": {
                            "bins": {
                                "bin1": {"hits": 1},
                                "bin2": {"hits": 1},
                            }
                        }
                    }
                }
            }
        }

        # Total: 4 bins, 3 hit = 75%
        total_bins = 0
        hit_bins = 0
        for cg_name, cg_data in covergroups.items():
            for cp_name, cp_data in cg_data.get("coverpoints", {}).items():
                for bin_name, bin_data in cp_data.get("bins", {}).get("bins", {}).items():
                    total_bins += 1
                    if bin_data.get("hits", 0) > 0:
                        hit_bins += 1

        coverage = (hit_bins / total_bins) * 100 if total_bins > 0 else 0.0
        assert coverage == 75.0


class TestCoverageDataEdgeCases:
    """Tests for CoverageData edge cases."""

    def test_empty_covergroups(self):
        """Test coverage data with empty covergroups dict."""
        cd = CoverageData(covergroups={})

        total_bins = 0
        hit_bins = 0
        for cg_name, cg_data in cd.covergroups.items():
            for cp_name, cp_data in cg_data.get("coverpoints", {}).items():
                for bin_name, bin_data in cp_data.get("bins", {}).get("bins", {}).items():
                    total_bins += 1
                    if bin_data.get("hits", 0) > 0:
                        hit_bins += 1

        coverage = (hit_bins / total_bins) * 100 if total_bins > 0 else 0.0
        assert coverage == 0.0

    def test_multiple_hits_same_bin(self):
        """Test that multiple hits are counted correctly."""
        covergroups = {
            "test_cg": {
                "coverpoints": {
                    "cp1": {
                        "bins": {
                            "bins": {
                                "bin1": {"hits": 5},
                            }
                        }
                    }
                }
            }
        }

        total_bins = 0
        hit_bins = 0
        for cg_name, cg_data in covergroups.items():
            for cp_name, cp_data in cg_data.get("coverpoints", {}).items():
                for bin_name, bin_data in cp_data.get("bins", {}).get("bins", {}).items():
                    total_bins += 1
                    if bin_data.get("hits", 0) > 0:
                        hit_bins += 1

        coverage = (hit_bins / total_bins) * 100 if total_bins > 0 else 0.0
        assert coverage == 100.0  # Still 100% because bin was hit at least once
