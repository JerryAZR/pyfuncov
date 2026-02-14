# pyfuncov

**pyfuncov** is a Python library for tracking functional coverage in tests, inspired by SystemVerilog's coverpoint and covergroup concepts.

## Features

- **Covergroups**: Group related coverpoints together for organized coverage tracking
- **Coverpoints**: Track values with discrete bins, range bins, or transition bins
- **Coverage Reports**: Generate JSON reports with coverage statistics
- **Persistent Storage**: Save and load coverage data to/from JSON files

## Installation

Install from Git:

```bash
pip install git+https://github.com/JerryAZR/pyfuncov.git
```

Or clone and install in development mode:

```bash
git clone https://github.com/JerryAZR/pyfuncov.git
cd pyfuncov
pip install -e .
```

## Quick Start

```python
from pyfuncov import Covergroup, Bin, BinKind

# Create a covergroup
cg = Covergroup(name="my_coverage", module="test")

# Add coverpoints with different bin types
cg.add_coverpoint(
    name="x",
    bins=[
        Bin(name="one", bin_type=BinKind.DISCRETE, value=1),
        Bin(name="two", bin_type=BinKind.DISCRETE, value=2),
        Bin(name="three", bin_type=BinKind.DISCRETE, value=3),
    ]
)

# Register the covergroup
cg.register()

# Sample values
cg.sample("x", 1)
cg.sample("x", 2)
cg.sample("x", 3)

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
