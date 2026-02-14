"""Unit tests for JSON storage module."""

import json
from datetime import datetime

import pytest

from pyfuncov.models.coverage_data import CoverageData
from pyfuncov.storage.json_storage import (
    load_coverage_from_file,
    merge_coverage_data,
    save_coverage_to_file,
)


class TestSaveCoverageToFile:
    """Tests for save_coverage_to_file function."""

    def test_save_coverage_produces_valid_json(self, tmp_path):
        """Test that save produces valid JSON."""
        filepath = tmp_path / "coverage.json"
        cd = CoverageData()
        cd.covergroups = {"test_cg": {"coverpoints": {}}}
        cd.total_runs = 1

        save_coverage_to_file(cd, str(filepath))

        assert filepath.exists()

        # Verify it's valid JSON
        with open(filepath, "r") as f:
            data = json.load(f)

        assert "version" in data
        assert "total_runs" in data
        assert "covergroups" in data

    def test_save_coverage_with_covergroup_data(self, tmp_path):
        """Test saving coverage with covergroup data."""
        filepath = tmp_path / "coverage.json"
        cd = CoverageData()
        cd.covergroups = {
            "test_cg": {
                "name": "test_cg",
                "coverpoints": {
                    "cp1": {
                        "name": "cp1",
                        "bins": {
                            "bins": {
                                "bin1": {"hits": 5}
                            }
                        }
                    }
                }
            }
        }
        cd.total_runs = 3

        save_coverage_to_file(cd, str(filepath))

        with open(filepath, "r") as f:
            data = json.load(f)

        assert data["total_runs"] == 3
        assert "test_cg" in data["covergroups"]

    def test_save_coverage_creates_parent_dirs(self, tmp_path):
        """Test that save creates parent directories if needed."""
        filepath = tmp_path / "subdir" / "nested" / "coverage.json"
        cd = CoverageData()

        save_coverage_to_file(cd, str(filepath))

        assert filepath.exists()

    def test_save_coverage_timestamp(self, tmp_path):
        """Test that save includes timestamp."""
        filepath = tmp_path / "coverage.json"
        cd = CoverageData()

        save_coverage_to_file(cd, str(filepath))

        with open(filepath, "r") as f:
            data = json.load(f)

        assert "last_updated" in data
        assert data["last_updated"] is not None


class TestLoadCoverageFromFile:
    """Tests for load_coverage_from_file function."""

    def test_load_coverage_restores_data(self, tmp_path):
        """Test loading coverage restores all data."""
        # Create a coverage file
        filepath = tmp_path / "coverage.json"
        original_data = {
            "version": "1.0",
            "total_runs": 5,
            "last_updated": "2024-01-01T00:00:00",
            "covergroups": {
                "test_cg": {
                    "name": "test_cg",
                    "coverpoints": {
                        "cp1": {
                            "bins": {
                                "bins": {
                                    "bin1": {"hits": 3}
                                }
                            }
                        }
                    }
                }
            }
        }

        with open(filepath, "w") as f:
            json.dump(original_data, f)

        loaded = load_coverage_from_file(str(filepath))

        assert loaded.version == "1.0"
        assert loaded.total_runs == 5
        assert "test_cg" in loaded.covergroups

    def test_load_nonexistent_file(self, tmp_path):
        """Test loading a nonexistent file raises FileNotFoundError."""
        filepath = tmp_path / "nonexistent.json"

        with pytest.raises(FileNotFoundError):
            load_coverage_from_file(str(filepath))

    def test_load_invalid_json(self, tmp_path):
        """Test loading corrupted JSON handles error gracefully."""
        filepath = tmp_path / "corrupted.json"
        filepath.write_text("{ invalid json }")

        # According to code, it returns empty CoverageData on parse error
        loaded = load_coverage_from_file(str(filepath))
        assert loaded.covergroups == {}
        assert loaded.total_runs == 0

    def test_load_missing_fields(self, tmp_path):
        """Test loading JSON with missing fields uses defaults."""
        filepath = tmp_path / "coverage.json"
        filepath.write_text("{}")

        loaded = load_coverage_from_file(str(filepath))

        assert loaded.version == "1.0"
        assert loaded.total_runs == 0
        assert loaded.covergroups == {}

    def test_load_invalid_timestamp(self, tmp_path):
        """Test loading with invalid timestamp handles gracefully."""
        filepath = tmp_path / "coverage.json"
        data = {
            "version": "1.0",
            "total_runs": 1,
            "last_updated": "invalid-timestamp",
            "covergroups": {}
        }

        with open(filepath, "w") as f:
            json.dump(data, f)

        loaded = load_coverage_from_file(str(filepath))
        # Should use current time as fallback
        assert loaded.last_updated is not None


class TestMergeCoverageData:
    """Tests for merge_coverage_data function."""

    def test_merge_coverage_data_adds_runs(self):
        """Test merging adds total runs."""
        existing = CoverageData(total_runs=2)
        new = CoverageData(total_runs=3)

        merged = merge_coverage_data(existing, new)

        assert merged.total_runs == 5

    def test_merge_coverage_data_new_covergroup(self):
        """Test merging adds new covergroup."""
        existing = CoverageData(covergroups={})
        new = CoverageData(covergroups={"cg1": {"name": "cg1"}})

        merged = merge_coverage_data(existing, new)

        assert "cg1" in merged.covergroups

    def test_merge_coverage_data_existing_covergroup(self):
        """Test merging accumulates hits for existing covergroup."""
        existing = CoverageData(covergroups={
            "cg1": {
                "coverpoints": {
                    "cp1": {
                        "bins": {
                            "bins": {
                                "bin1": {"hits": 2}
                            }
                        }
                    }
                }
            }
        })

        new = CoverageData(covergroups={
            "cg1": {
                "coverpoints": {
                    "cp1": {
                        "bins": {
                            "bins": {
                                "bin1": {"hits": 3}
                            }
                        }
                    }
                }
            }
        })

        merged = merge_coverage_data(existing, new)

        # Hits should be accumulated
        merged_hits = merged.covergroups["cg1"]["coverpoints"]["cp1"]["bins"]["bins"]["bin1"]["hits"]
        assert merged_hits == 5

    def test_merge_coverage_data_preserves_version(self):
        """Test merging preserves existing version."""
        existing = CoverageData(version="2.0")
        new = CoverageData(version="1.0")

        merged = merge_coverage_data(existing, new)

        assert merged.version == "2.0"

    def test_merge_coverage_data_multiple_covergroups(self):
        """Test merging multiple covergroups."""
        existing = CoverageData(covergroups={
            "cg1": {"coverpoints": {}},
            "cg2": {"coverpoints": {}}
        })
        new = CoverageData(covergroups={
            "cg3": {"coverpoints": {}}
        })

        merged = merge_coverage_data(existing, new)

        assert len(merged.covergroups) == 3
        assert "cg1" in merged.covergroups
        assert "cg2" in merged.covergroups
        assert "cg3" in merged.covergroups


class TestSerializeDatetime:
    """Tests for datetime serialization."""

    def test_serialize_datetime_to_isoformat(self, tmp_path):
        """Test datetime is serialized to ISO format."""
        from pyfuncov.storage.json_storage import _serialize_datetime

        # Test direct call to function
        result = _serialize_datetime(datetime(2024, 6, 15, 10, 30, 0))
        assert "2024-06-15" in result

        # Also test through save_coverage_to_file
        filepath = tmp_path / "coverage.json"
        cd = CoverageData()
        cd.last_updated = datetime(2024, 6, 15, 10, 30, 0)
        save_coverage_to_file(cd, str(filepath))

        with open(filepath, "r") as f:
            data = json.load(f)

        assert "2024-06-15" in data["last_updated"]

    def test_serialize_invalid_type(self, tmp_path):
        """Test serialization raises TypeError for non-serializable types."""
        from pyfuncov.storage.json_storage import _serialize_datetime

        with pytest.raises(TypeError):
            _serialize_datetime("not a datetime")


class TestMergeCoverageDataEdgeCases:
    """Tests for merge_coverage_data edge cases."""

    def test_merge_covergroup_without_coverpoints(self):
        """Test merging when existing covergroup has no coverpoints key."""
        existing = CoverageData(covergroups={
            "cg1": {}  # No coverpoints key
        })
        new = CoverageData(covergroups={
            "cg1": {
                "coverpoints": {
                    "cp1": {
                        "bins": {
                            "bins": {
                                "bin1": {"hits": 1}
                            }
                        }
                    }
                }
            }
        })

        merged = merge_coverage_data(existing, new)
        assert "cp1" in merged.covergroups["cg1"]["coverpoints"]

    def test_merge_new_bin_in_existing_coverpoint(self):
        """Test merging adds new bins to existing coverpoint."""
        existing = CoverageData(covergroups={
            "cg1": {
                "coverpoints": {
                    "cp1": {
                        "bins": {
                            "bins": {
                                "bin1": {"hits": 2}
                            }
                        }
                    }
                }
            }
        })
        new = CoverageData(covergroups={
            "cg1": {
                "coverpoints": {
                    "cp1": {
                        "bins": {
                            "bins": {
                                "bin2": {"hits": 1}
                            }
                        }
                    }
                }
            }
        })

        merged = merge_coverage_data(existing, new)
        # Should have both bins
        assert "bin1" in merged.covergroups["cg1"]["coverpoints"]["cp1"]["bins"]["bins"]
        assert "bin2" in merged.covergroups["cg1"]["coverpoints"]["cp1"]["bins"]["bins"]

    def test_merge_new_bin_in_existing_coverpoint_no_bins_key(self):
        """Test merging when existing coverpoint has no bins key."""
        existing = CoverageData(covergroups={
            "cg1": {
                "coverpoints": {
                    "cp1": {}  # No bins key at all
                }
            }
        })
        new = CoverageData(covergroups={
            "cg1": {
                "coverpoints": {
                    "cp1": {
                        "bins": {
                            "bins": {
                                "bin1": {"hits": 1}
                            }
                        }
                    }
                }
            }
        })

        merged = merge_coverage_data(existing, new)
        # Should have the new bin
        assert "bin1" in merged.covergroups["cg1"]["coverpoints"]["cp1"]["bins"]["bins"]

    def test_merge_adds_coverpoint_to_existing_cg(self):
        """Test merging adds new coverpoint to existing covergroup."""
        existing = CoverageData(covergroups={
            "cg1": {
                "coverpoints": {
                    "cp1": {
                        "bins": {"bins": {"bin1": {"hits": 1}}}
                    }
                }
            }
        })
        new = CoverageData(covergroups={
            "cg1": {
                "coverpoints": {
                    "cp2": {
                        "bins": {"bins": {"bin1": {"hits": 1}}}
                    }
                }
            }
        })

        merged = merge_coverage_data(existing, new)
        assert "cp1" in merged.covergroups["cg1"]["coverpoints"]
        assert "cp2" in merged.covergroups["cg1"]["coverpoints"]
