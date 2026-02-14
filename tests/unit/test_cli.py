"""Unit tests for CLI module."""

import json
import sys
from io import StringIO

import pytest

from pyfuncov.cli import main


class TestCLIMainEntryPoint:
    """Tests for CLI main entry point."""

    def test_main_no_args_shows_help(self, capsys):
        """Test main with no arguments shows help."""
        # Save original argv and stdin
        original_argv = sys.argv
        original_stdin = sys.stdin

        try:
            sys.argv = ["pyfuncov"]
            sys.stdin = StringIO()

            # Patch sys.exit to prevent actual exit
            with pytest.raises(SystemExit):
                main()
        finally:
            sys.argv = original_argv
            sys.stdin = original_stdin

    def test_main_help_flag(self, capsys):
        """Test main with --help shows help."""
        original_argv = sys.argv
        original_stderr = sys.stderr

        try:
            sys.argv = ["pyfuncov", "--help"]
            sys.stderr = StringIO()

            with pytest.raises(SystemExit):
                main()
        finally:
            sys.argv = original_argv
            sys.stderr = original_stderr


class TestCLIReportCommand:
    """Tests for report command."""

    def test_report_command_missing_file(self, capsys):
        """Test report command with missing file."""
        original_argv = sys.argv

        try:
            sys.argv = ["pyfuncov", "report", "nonexistent.json"]

            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1
        finally:
            sys.argv = original_argv

    def test_report_command_with_valid_file(self, tmp_path, capsys):
        """Test report command with valid coverage file."""
        # Create a valid coverage file
        coverage_file = tmp_path / "coverage.json"
        data = {
            "version": "1.0",
            "total_runs": 1,
            "last_updated": "2024-01-01T00:00:00",
            "covergroups": {
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
            }
        }

        with open(coverage_file, "w") as f:
            json.dump(data, f)

        original_argv = sys.argv

        try:
            sys.argv = ["pyfuncov", "report", str(coverage_file)]
            main()
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        assert "Coverage Report" in captured.out or "cg1" in captured.out

    def test_report_command_json_format(self, tmp_path, capsys):
        """Test report command with JSON format."""
        # Create a valid coverage file
        coverage_file = tmp_path / "coverage.json"
        data = {
            "version": "1.0",
            "total_runs": 1,
            "last_updated": "2024-01-01T00:00:00",
            "covergroups": {}
        }

        with open(coverage_file, "w") as f:
            json.dump(data, f)

        original_argv = sys.argv

        try:
            sys.argv = ["pyfuncov", "report", str(coverage_file), "--format", "json"]
            main()
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        # Should be valid JSON output
        output = captured.out.strip()
        if output:
            parsed = json.loads(output)
            assert "overall_coverage" in parsed



class TestCLIDiffCommand:
    """Tests for diff command."""

    def test_diff_command_missing_baseline(self, tmp_path, capsys):
        """Test diff command with missing baseline file."""
        current_file = tmp_path / "current.json"
        current_file.write_text("{}")

        original_argv = sys.argv

        try:
            sys.argv = ["pyfuncov", "diff", "nonexistent.json", str(current_file)]

            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1
        finally:
            sys.argv = original_argv

    def test_diff_command_missing_current(self, tmp_path, capsys):
        """Test diff command with missing current file."""
        baseline_file = tmp_path / "baseline.json"
        baseline_file.write_text("{}")

        original_argv = sys.argv

        try:
            sys.argv = ["pyfuncov", "diff", str(baseline_file), "nonexistent.json"]

            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1
        finally:
            sys.argv = original_argv

    def test_diff_command_with_valid_files(self, tmp_path, capsys):
        """Test diff command with valid coverage files."""
        baseline_file = tmp_path / "baseline.json"
        current_file = tmp_path / "current.json"

        baseline_data = {
            "covergroups": {
                "cg1": {
                    "coverpoints": {
                        "cp1": {
                            "bins": {
                                "bins": {
                                    "bin1": {"hits": 1},
                                    "bin2": {"hits": 0}
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
                                    "bin2": {"hits": 1}
                                }
                            }
                        }
                    }
                }
            }
        }

        with open(baseline_file, "w") as f:
            json.dump(baseline_data, f)

        with open(current_file, "w") as f:
            json.dump(current_data, f)

        original_argv = sys.argv

        try:
            sys.argv = ["pyfuncov", "diff", str(baseline_file), str(current_file)]
            main()
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        assert "Coverage Comparison" in captured.out

    def test_diff_command_shows_regressions(self, tmp_path, capsys):
        """Test diff command shows regressions when coverage decreases."""
        baseline_file = tmp_path / "baseline.json"
        current_file = tmp_path / "current.json"

        # Baseline: 100% coverage
        baseline_data = {
            "covergroups": {
                "cg1": {
                    "coverpoints": {
                        "cp1": {
                            "bins": {
                                "bins": {
                                    "bin1": {"hits": 1},
                                    "bin2": {"hits": 1}
                                }
                            }
                        }
                    }
                }
            }
        }

        # Current: 50% coverage (regression)
        current_data = {
            "covergroups": {
                "cg1": {
                    "coverpoints": {
                        "cp1": {
                            "bins": {
                                "bins": {
                                    "bin1": {"hits": 1},
                                    "bin2": {"hits": 0}
                                }
                            }
                        }
                    }
                }
            }
        }

        with open(baseline_file, "w") as f:
            json.dump(baseline_data, f)

        with open(current_file, "w") as f:
            json.dump(current_data, f)

        original_argv = sys.argv

        try:
            sys.argv = ["pyfuncov", "diff", str(baseline_file), str(current_file)]
            main()
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        assert "Regressions:" in captured.out

    def test_diff_command_shows_improvements(self, tmp_path, capsys):
        """Test diff command shows improvements when coverage increases."""
        baseline_file = tmp_path / "baseline.json"
        current_file = tmp_path / "current.json"

        # Baseline: 50% coverage
        baseline_data = {
            "covergroups": {
                "cg1": {
                    "coverpoints": {
                        "cp1": {
                            "bins": {
                                "bins": {
                                    "bin1": {"hits": 1},
                                    "bin2": {"hits": 0}
                                }
                            }
                        }
                    }
                }
            }
        }

        # Current: 100% coverage (improvement)
        current_data = {
            "covergroups": {
                "cg1": {
                    "coverpoints": {
                        "cp1": {
                            "bins": {
                                "bins": {
                                    "bin1": {"hits": 1},
                                    "bin2": {"hits": 1}
                                }
                            }
                        }
                    }
                }
            }
        }

        with open(baseline_file, "w") as f:
            json.dump(baseline_data, f)

        with open(current_file, "w") as f:
            json.dump(current_data, f)

        original_argv = sys.argv

        try:
            sys.argv = ["pyfuncov", "diff", str(baseline_file), str(current_file)]
            main()
        finally:
            sys.argv = original_argv

        captured = capsys.readouterr()
        assert "Improvements:" in captured.out


class TestCLISubcommands:
    """Tests for CLI subcommands."""

    def test_subcommand_report_exists(self, capsys):
        """Test report subcommand exists."""
        original_argv = sys.argv

        try:
            sys.argv = ["pyfuncov", "report", "--help"]
            sys.stderr = StringIO()

            with pytest.raises(SystemExit):
                main()
        finally:
            sys.argv = original_argv
            sys.stderr = StringIO()

    def test_subcommand_diff_exists(self, capsys):
        """Test diff subcommand exists."""
        original_argv = sys.argv

        try:
            sys.argv = ["pyfuncov", "diff", "--help"]
            sys.stderr = StringIO()

            with pytest.raises(SystemExit):
                main()
        finally:
            sys.argv = original_argv


class TestCLIErrorHandling:
    """Tests for CLI error handling."""

    def test_invalid_subcommand(self, capsys):
        """Test invalid subcommand shows error."""
        original_argv = sys.argv

        try:
            sys.argv = ["pyfuncov", "invalid_command"]
            sys.stderr = StringIO()

            with pytest.raises(SystemExit) as exc_info:
                main()

            # Should exit with error (exit code 2 for argparse errors)
            assert exc_info.value.code == 2
        finally:
            sys.argv = original_argv
