# Getting Started

This guide will help you get started with pyfuncov in about 10 minutes.

## Prerequisites

- Python 3.10 or higher
- pip package manager

## Installation

Clone and install in development mode:

```bash
git clone https://github.com/JerryAZR/pyfuncov.git
cd pyfuncov
pip install -e .[dev]
```

## Your First Coverage Test

Create a Python file and add the following code:

```python
from pyfuncov import Covergroup, Bin, BinKind, save_coverage, load_coverage, get_coverage_data, generate_report

# Create a covergroup
cg = Covergroup(name="my_coverage", module="test")

# Add coverpoints with discrete bins
cg.add_coverpoint(
    name="x",
    bins=[
        Bin(name="one", bin_type=BinKind.DISCRETE, value=1),
        Bin(name="two", bin_type=BinKind.DISCRETE, value=2),
        Bin(name="three", bin_type=BinKind.DISCRETE, value=3),
        Bin(name="four", bin_type=BinKind.DISCRETE, value=4),
        Bin(name="five", bin_type=BinKind.DISCRETE, value=5),
    ]
)

# Register the covergroup
cg.register()

# Sample some values
cg.sample("x", 1)
cg.sample("x", 3)
cg.sample("x", 5)

# Save coverage and generate report
save_coverage("coverage.json")
load_coverage("coverage.json")
data = get_coverage_data()
print(generate_report("text", {"covergroups": data.covergroups}))
```

## Viewing Documentation Offline

You can view the documentation offline by serving it locally:

```bash
# Install documentation dependencies (if not already installed)
uv sync --group docs

# Serve documentation locally
uv run --directory docs mkdocs serve

# Open your browser to http://localhost:8000
```

The documentation will be available at `http://localhost:8000` in your browser.

## Next Steps

- Read the [Covergroups Guide](guides/covergroup.md) to learn more about covergroups
- Read the [Coverpoints Guide](guides/coverpoint.md) to understand different bin types
- Explore the [API Reference](api/index.md) for detailed documentation
