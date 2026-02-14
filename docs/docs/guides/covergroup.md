# Covergroups

Covergroups are the main container for organizing related coverage points in pyfuncov. They work similarly to SystemVerilog covergroups.

## Creating a Covergroup

```python
from pyfuncov import Covergroup

# Create a new covergroup
cg = Covergroup(name="my_coverage", module="test")
```

## Adding Coverpoints

Coverpoints define what values you want to track:

```python
from pyfuncov import Bin, BinKind

# Add a coverpoint with discrete bins
cg.add_coverpoint(
    name="x",
    bins=[
        Bin(name="one", bin_type=BinKind.DISCRETE, value=1),
        Bin(name="two", bin_type=BinKind.DISCRETE, value=2),
    ]
)

# Add a coverpoint with range bins
cg.add_coverpoint(
    name="y",
    bins=[
        Bin(name="low", bin_type=BinKind.RANGE, range_min=0, range_max=10),
        Bin(name="high", bin_type=BinKind.RANGE, range_min=10, range_max=20),
    ]
)
```

## Registering a Covergroup

Before sampling values, you must register the covergroup:

```python
cg.register()
```

## Sampling Values

Use the `sample()` method to record values:

```python
cg.sample("x", 1)  # Record value 1 for coverpoint "x"
cg.sample("y", 15)  # Record value 15 for coverpoint "y"
```

## Getting Coverage Reports

Generate a coverage report at any time:

```python
report = cg.report()
print(report)
```

## Complete Example

```python
from pyfuncov import Covergroup, Bin, BinKind

# Create and configure covergroup
cg = Covergroup(name="example", module="test")
cg.add_coverpoint(
    name="mode",
    bins=[
        Bin(name="read", bin_type=BinKind.DISCRETE, value="read"),
        Bin(name="write", bin_type=BinKind.DISCRETE, value="write"),
        Bin(name="idle", bin_type=BinKind.DISCRETE, value="idle"),
    ]
)
cg.add_coverpoint(
    name="address",
    bins=[
        Bin(name="low", bin_type=BinKind.RANGE, range_min=0, range_max=256),
        Bin(name="high", bin_type=BinKind.RANGE, range_min=256, range_max=512),
    ]
)

# Register before sampling
cg.register()

# Sample values
cg.sample("mode", "read")
cg.sample("mode", "write")
cg.sample("address", 100)

# Get report
print(cg.report())
```

## Methods

| Method | Description |
|--------|-------------|
| `add_coverpoint(name, bins)` | Add a coverpoint with specified bins |
| `register(module=None)` | Register the covergroup before sampling |
| `sample(name, value)` | Record a sampled value |
| `report()` | Generate coverage report |
