"""Pytest configuration and fixtures for pyfuncov tests."""

import pytest

from pyfuncov.models.covergroup import clear_registry
from pyfuncov.storage import reset_coverage_data


@pytest.fixture(autouse=True)
def clean_pyfuncov_state():
    """Clean up pyfuncov global state before and after each test."""
    clear_registry()
    reset_coverage_data()
    yield
    clear_registry()
    reset_coverage_data()
