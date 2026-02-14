# pyfuncov

**pyfuncov** is a Python library for tracking functional coverage in tests, inspired by SystemVerilog's coverpoint and covergroup concepts.

## Features

- **Covergroups**: Group related coverpoints together for organized coverage tracking
- **Coverpoints**: Track values with discrete bins, range bins, or transition bins
- **Coverage Reports**: Generate JSON reports with coverage statistics
- **Persistent Storage**: Save and load coverage data to/from JSON files

## Installation

```bash
pip install pyfuncov
```

## Quick Start

```python
from pyfuncov import Covergroup, Coverpoint

# Create a covergroup
cg = Covergroup("my_coverage")

# Add coverpoints with different bin types
cg.coverpoint("x", bins=[1, 2, 3, 4, 5])  # Discrete bins
cg.coverpoint("y", bins={"low": range(0, 10), "high": range(10, 20)})  # Range bins

# Register the covergroup
cg.register()

# Sample values
cg.sample("x", 3)
cg.sample("y", 15)

# Get coverage report
print(cg.report())
```

## Documentation

- [Getting Started](getting-started.md) - Begin your journey here
- [Covergroups Guide](guides/covergroup.md) - Learn about covergroups
- [Coverpoints Guide](guides/coverpoint.md) - Understand bins and sampling
- [API Reference](api/index.md) - Detailed API documentation

## License

MIT License - see [GitHub repository](https://github.com/JerryAZR/pyfuncov) for details.
