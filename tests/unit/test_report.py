"""Unit tests for core report generation module."""

import json

import pytest

from pyfuncov.core.report import (
    CovergroupReport,
    CoverageReport,
    calculate_coverage,
    compare_reports,
    generate_json_report,
    generate_report,
    generate_text_report,
)


class TestCalculateCoverage:
    """Tests for calculate_coverage function."""

    def test_calculate_coverage_with_bins_hit(self):
        """Test coverage calculation with some bins hit."""
        cg_data = {
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

        coverage, total, hit, missed = calculate_coverage(cg_data)

        assert coverage == pytest.approx(66.67, rel=0.1)
        assert total == 3
        assert hit == 2
        assert "bin2" in missed

    def test_calculate_coverage_all_bins_hit(self):
        """Test coverage calculation with all bins hit."""
        cg_data = {
            "coverpoints": {
                "cp1": {
                    "bins": {
                        "bins": {
                            "bin1": {"hits": 1},
                            "bin2": {"hits": 2},
                        }
                    }
                }
            }
        }

        coverage, total, hit, missed = calculate_coverage(cg_data)

        assert coverage == 100.0
        assert total == 2
        assert hit == 2
        assert missed == []

    def test_calculate_coverage_no_bins_hit(self):
        """Test coverage calculation with no bins hit."""
        cg_data = {
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

        coverage, total, hit, missed = calculate_coverage(cg_data)

        assert coverage == 0.0
        assert total == 2
        assert hit == 0
        assert len(missed) == 2

    def test_calculate_coverage_no_bins_defined(self):
        """Test coverage calculation with no bins defined."""
        cg_data = {
            "coverpoints": {}
        }

        coverage, total, hit, missed = calculate_coverage(cg_data)

        assert coverage == 0.0
        assert total == 0
        assert hit == 0
        assert missed == []

    def test_calculate_coverage_empty_data(self):
        """Test coverage calculation with empty data."""
        coverage, total, hit, missed = calculate_coverage({})

        assert coverage == 0.0
        assert total == 0
        assert hit == 0
        assert missed == []


class TestGenerateTextReport:
    """Tests for generate_text_report function."""

    def test_generate_text_report_multiple_covergroups(self):
        """Test text report generation with multiple covergroups."""
        coverage_data = {
            "covergroups": {
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
        }

        report = generate_text_report(coverage_data)

        assert "Coverage Report" in report
        assert "cg1" in report
        assert "cg2" in report
        assert "Overall Coverage" in report
        assert "Missed Bins" in report

    def test_generate_text_report_correct_bin_hit_counts(self):
        """Test text report has correct bin hit counts."""
        coverage_data = {
            "covergroups": {
                "test_cg": {
                    "coverpoints": {
                        "cp1": {
                            "bins": {
                                "bins": {
                                    "bin1": {"hits": 5},
                                    "bin2": {"hits": 0},
                                }
                            }
                        }
                    }
                }
            }
        }

        report = generate_text_report(coverage_data)

        # Should show 1/2 bins hit
        assert "1/2 bins" in report

    def test_generate_text_report_empty_data(self):
        """Test text report with empty coverage data."""
        report = generate_text_report({})

        assert "Coverage Report" in report
        assert "Overall Coverage" in report
        assert "0.00%" in report


class TestGenerateJsonReport:
    """Tests for generate_json_report function."""

    def test_generate_json_report_valid_json(self):
        """Test JSON report produces valid JSON."""
        coverage_data = {
            "covergroups": {
                "test_cg": {
                    "coverpoints": {
                        "cp1": {
                            "bins": {
                                "bins": {
                                    "bin1": {"hits": 1},
                                }
                            }
                        }
                    }
                }
            }
        }

        report_json = generate_json_report(coverage_data)

        # Verify it's valid JSON
        report = json.loads(report_json)
        assert "overall_coverage" in report
        assert "covergroups" in report

    def test_generate_json_report_structure(self):
        """Test JSON report has correct structure."""
        coverage_data = {
            "covergroups": {
                "cg1": {
                    "coverpoints": {
                        "cp1": {
                            "bins": {
                                "bins": {
                                    "bin1": {"hits": 1},
                                }
                            }
                        }
                    }
                }
            }
        }

        report_json = generate_json_report(coverage_data, version="1.0")
        report = json.loads(report_json)

        assert report["version"] == "1.0"
        assert "total_bins" in report
        assert "hit_bins" in report
        assert "missed_bins" in report
        assert "generated_at" in report
        assert len(report["covergroups"]) == 1


class TestGenerateReport:
    """Tests for generate_report function."""

    def test_generate_report_text_format(self):
        """Test generate_report with text format."""
        coverage_data = {
            "covergroups": {
                "cg1": {
                    "coverpoints": {
                        "cp1": {
                            "bins": {
                                "bins": {
                                    "bin1": {"hits": 1},
                                }
                            }
                        }
                    }
                }
            }
        }

        report = generate_report(format="text", data=coverage_data)
        assert "Coverage Report" in report

    def test_generate_report_json_format(self):
        """Test generate_report with JSON format."""
        coverage_data = {
            "covergroups": {}
        }

        report = generate_report(format="json", data=coverage_data)
        parsed = json.loads(report)
        assert "overall_coverage" in parsed

    def test_generate_report_none_data(self):
        """Test generate_report with None data."""
        report = generate_report(format="text", data=None)
        assert "Coverage Report" in report

        report_json = generate_report(format="json", data=None)
        parsed = json.loads(report_json)
        assert parsed["overall_coverage"] == 0.0


class TestCompareReports:
    """Tests for compare_reports function."""

    def test_compare_reports_improvement(self):
        """Test comparing reports with improvement."""
        baseline_data = {
            "covergroups": {
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
                }
            }
        }

        current_data = {
            "covergroups": {
                "cg1": {
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
        }

        result = compare_reports(baseline_data, current_data)

        assert result["baseline_overall"] == pytest.approx(50.0)
        assert result["current_overall"] == 100.0
        assert result["difference"] == pytest.approx(50.0)
        assert len(result["improvements"]) == 1

    def test_compare_reports_regression(self):
        """Test comparing reports with regression."""
        baseline_data = {
            "covergroups": {
                "cg1": {
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
        }

        current_data = {
            "covergroups": {
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
                }
            }
        }

        result = compare_reports(baseline_data, current_data)

        assert result["baseline_overall"] == 100.0
        assert result["current_overall"] == pytest.approx(50.0)
        assert result["difference"] == pytest.approx(-50.0)
        assert len(result["regressions"]) == 1

    def test_compare_reports_no_change(self):
        """Test comparing reports with no change."""
        data = {
            "covergroups": {
                "cg1": {
                    "coverpoints": {
                        "cp1": {
                            "bins": {
                                "bins": {
                                    "bin1": {"hits": 1},
                                }
                            }
                        }
                    }
                }
            }
        }

        result = compare_reports(data, data)

        assert result["difference"] == 0.0
        assert result["regressions"] == []
        assert result["improvements"] == []

    def test_compare_reports_empty_data(self):
        """Test comparing with empty data."""
        result = compare_reports({}, {})

        assert result["baseline_overall"] == 0.0
        assert result["current_overall"] == 0.0
        assert result["difference"] == 0.0


class TestCovergroupReport:
    """Tests for CovergroupReport dataclass."""

    def test_covergroup_report_creation(self):
        """Test creating a CovergroupReport."""
        report = CovergroupReport(
            name="test_cg",
            coverage=75.0,
            total_bins=4,
            hit_bins=3,
            coverpoints=[],
            missed_bins=["bin4"]
        )

        assert report.name == "test_cg"
        assert report.coverage == 75.0
        assert report.total_bins == 4
        assert report.hit_bins == 3
        assert report.missed_bins == ["bin4"]


class TestCoverageReport:
    """Tests for CoverageReport dataclass."""

    def test_coverage_report_creation(self):
        """Test creating a CoverageReport."""
        from datetime import datetime

        report = CoverageReport(
            overall_coverage=85.0,
            covergroups=[],
            missed_bins=[],
            generated_at=datetime.now(),
            version="1.0"
        )

        assert report.overall_coverage == 85.0
        assert report.version == "1.0"
