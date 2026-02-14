# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pyfuncov is a Python functional coverage tracking library inspired by SystemVerilog's coverpoint/covergroup concepts. It provides tools for measuring functional coverage in tests, with support for discrete bins, range bins, and transition bins.

## Commands

```bash
# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Run a single test file
pytest tests/unit/test_bin.py

# Run linter
ruff check .
```

## Architecture

```text
src/pyfuncov/
├── models/          # Data models (Covergroup, Coverpoint, Bin, CoverageData)
├── core/            # Core functionality (report generation)
├── storage/         # JSON persistence layer
└── cli/             # Command-line interface
```

The library uses a global coverage registry. Covergroups are registered via `cg.register()` and values are sampled via `cg.sample(name, value)`.

## Testing

Tests are in `tests/` with unit tests in `tests/unit/` and integration tests in `tests/integration/`. Test configuration is in `pyproject.toml`.
