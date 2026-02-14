# Getting Started

This guide will help you get started with pyfuncov in about 10 minutes.

## Prerequisites

- Python 3.10 or higher
- pip package manager

## Installation

Install pyfuncov from Git:

```bash
pip install git+https://github.com/JerryAZR/pyfuncov.git
```

Or clone and install in development mode:

```bash
git clone https://github.com/JerryAZR/pyfuncov.git
cd pyfuncov
pip install -e .
```

## Your First Coverage Test

Create a Python file and add the following code:

```python
from pyfuncov import Covergroup, Bin, BinKind

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

# Get the coverage report
print(cg.report())
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
