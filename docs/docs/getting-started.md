# Getting Started

This guide will help you get started with pyfuncov in about 10 minutes.

## Prerequisites

- Python 3.10 or higher
- pip package manager

## Installation

Install pyfuncov using pip:

```bash
pip install pyfuncov
```

## Your First Coverage Test

Create a Python file and add the following code:

```python
from pyfuncov import Covergroup

# Create a covergroup
cg = Covergroup("my_coverage")

# Add coverpoints with discrete bins
cg.coverpoint("x", bins=[1, 2, 3, 4, 5])

# Register the covergroup
cg.register()

# Sample some values
cg.sample("x", 1)
cg.sample("x", 3)
cg.sample("x", 5)

# Get the coverage report
print(cg.report())
```

## Expected Output

```json
{
  "my_coverage": {
    "x": {
      "bins": {
        "1": 1,
        "2": 0,
        "3": 1,
        "4": 0,
        "5": 1
      },
      "total_hits": 3,
      "coverage_percent": 60.0
    }
  }
}
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
