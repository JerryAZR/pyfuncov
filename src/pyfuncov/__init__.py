"""pyfuncov - Python Functional Coverage Tool.

A Python functional coverage tracking tool inspired by SystemVerilog's
coverpoint/covergroup concepts. Provides a library interface for test
integration and CLI for reporting/analysis.
"""

from pyfuncov.core.report import (
    compare_reports,
    generate_json_report,
    generate_report,
    generate_text_report,
)
from pyfuncov.models.bin import Bin
from pyfuncov.models.coverage_data import CoverageData
from pyfuncov.models.covergroup import Covergroup, get_all_covergroups, get_covergroup
from pyfuncov.models.coverpoint import Coverpoint
from pyfuncov.models.enums import BinKind, OutOfBoundsMode
from pyfuncov.storage import get_coverage_data, load_coverage, reset_coverage_data, save_coverage

__version__ = "0.1.0"

__all__ = [
    # Models
    "Bin",
    "Covergroup",
    "Coverpoint",
    "CoverageData",
    # Enums
    "BinKind",
    "OutOfBoundsMode",
    # Storage
    "save_coverage",
    "load_coverage",
    "get_coverage_data",
    "reset_coverage_data",
    # Reports
    "generate_report",
    "generate_text_report",
    "generate_json_report",
    "compare_reports",
    # Registry
    "get_covergroup",
    "get_all_covergroups",
]
