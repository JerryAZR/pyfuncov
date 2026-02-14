# pyfuncov - Python Functional Coverage Tool

A Python functional coverage tracking library inspired by SystemVerilog's coverpoint/covergroup concepts. Provides a library interface for test integration and CLI for reporting/analysis.

## Features

- **Covergroups**: Named containers for related coverage points that define coverage domains
- **Coverpoints**: Individual coverage measurement points within a covergroup
- **Bins**: Discrete values, ranges, or transitions that track which values have been exercised
- **Multiple Bin Types**:
  - Discrete bins: Specific single values
  - Range bins: Value ranges (e.g., `[0:10]`)
  - Transition bins: Value transitions (e.g., `1->2->3`)
- **Persistence**: Save and load coverage data to JSON
- **Reporting**: Generate text or JSON coverage reports
- **Diff**: Compare coverage between baseline and current runs

## Installation

```bash
pip install pyfuncov
```

Or install from source:

```bash
git clone https://github.com/JerryAZR/pyfuncov.git
cd pyfuncov
pip install -e .
```

## Quick Start

```python
from pyfuncov import Covergroup, Coverpoint, Bin, BinKind, save_coverage, generate_text_report

# Create a covergroup
cg = Covergroup(name="parser", module="myapp")

# Add a coverpoint with discrete bins
cg.add_coverpoint(
    name="token_type",
    bins=[
        Bin(name="tok_plus", bin_type=BinKind.DISCRETE, value=1),
        Bin(name="tok_minus", bin_type=BinKind.DISCRETE, value=2),
        Bin(name="tok_mul", bin_type=BinKind.DISCRETE, value=3),
    ]
)

# Add a coverpoint with range bins
cg.add_coverpoint(
    name="value_range",
    bins=[
        Bin(name="low", bin_type=BinKind.RANGE, range_min=0, range_max=10),
        Bin(name="mid", bin_type=BinKind.RANGE, range_min=11, range_max=100),
        Bin(name="high", bin_type=BinKind.RANGE, range_min=101, range_max=1000),
    ]
)

# Register the covergroup
cg.register()

# Sample values during testing
cg.sample("token_type", 1)  # hits tok_plus
cg.sample("token_type", 2)  # hits tok_minus
cg.sample("value_range", 5)  # hits low
cg.sample("value_range", 50)  # hits mid
cg.sample("value_range", 500)  # hits high

# Save coverage data
save_coverage("coverage.json")

# Generate report
print(generate_text_report())
```

## CLI Usage

Generate a coverage report:

```bash
pyfuncov report coverage.json
pyfuncov report coverage.json --format json
```

Compare two coverage runs:

```bash
pyfuncov diff baseline.json current.json
```

## API Reference

### Core Classes

- `Covergroup`: Container for related coverage points
- `Coverpoint`: Individual coverage measurement point
- `Bin`: Tracks hits for specific values, ranges, or transitions

### Enums

- `BinKind`: DISCRETE, RANGE, TRANSITION
- `BinKind`: IGNORE, WARN, ERROR

### Storage Functions

- `save_coverage(filepath)`: Save coverage data to JSON
- `load_coverage(filepath)`: Load coverage data from JSON
- `get_coverage_data()`: Get current coverage data
- `reset_coverage_data()`: Reset coverage data

### Report Functions

- `generate_text_report()`: Generate human-readable report
- `generate_json_report()`: Generate JSON report
- `compare_reports(baseline, current)`: Compare two coverage runs

## License

MIT License
