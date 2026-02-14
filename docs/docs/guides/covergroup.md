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

Generate a coverage report using the storage and report functions:

```python
from pyfuncov import save_coverage, load_coverage, get_coverage_data, generate_report

# Save coverage data to a file
save_coverage("coverage.json")

# Load coverage data and generate a report
load_coverage("coverage.json")
data = get_coverage_data()
report = generate_report("text", {"covergroups": data.covergroups})
print(report)
```

## Complete Example

```python
from pyfuncov import Covergroup, Bin, BinKind, save_coverage, load_coverage, get_coverage_data, generate_report

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

# Save and generate report
save_coverage("coverage.json")
load_coverage("coverage.json")
data = get_coverage_data()
print(generate_report("text", {"covergroups": data.covergroups}))
```

## Methods

| Method | Description |
|--------|-------------|
| `add_coverpoint(name, bins, out_of_bounds)` | Add a coverpoint with specified bins |
| `register(module=None)` | Register the covergroup before sampling |
| `sample(name, value)` | Record a sampled value |

## Handling Out-of-Bounds Values

The `add_coverpoint` method accepts an `out_of_bounds` parameter to control how values outside the defined bins are handled:

```python
from pyfuncov import OutOfBoundsMode

# IGNORE (default): Don't track, continue silently
cg.add_coverpoint(name="x", bins=[...], out_of_bounds=OutOfBoundsMode.IGNORE)

# WARN: Log a warning, continue silently
cg.add_coverpoint(name="x", bins=[...], out_of_bounds=OutOfBoundsMode.WARN)

# ERROR: Raise an exception
cg.add_coverpoint(name="x", bins=[...], out_of_bounds=OutOfBoundsMode.ERROR)
```
