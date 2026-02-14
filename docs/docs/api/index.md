# API Reference

This section contains auto-generated API documentation for pyfuncov.

## Modules

| Module | Description |
|--------|-------------|
| [Covergroup](covergroup.md) | Main coverage tracking container |
| [Coverpoint](coverpoint.md) | Individual coverage point with bins |
| [Bin](bin.md) | Bin definition for value tracking |
| [CoverageData](coverage_data.md) | Coverage data storage and reporting |

## Usage

The API reference is auto-generated from the source code docstrings using [mkdocstrings](https://mkdocstrings.org/).

```python
# Example: Using the API
from pyfuncov import Covergroup

cg = Covergroup("example")
cg.coverpoint("x", bins=[1, 2, 3])
cg.register()
cg.sample("x", 2)
print(cg.report())
```
