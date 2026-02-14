# Covergroups

Covergroups are the main container for organizing related coverage points in pyfuncov. They work similarly to SystemVerilog covergroups.

## Creating a Covergroup

```python
from pyfuncov import Covergroup

# Create a new covergroup
cg = Covergroup("my_coverage")
```

## Adding Coverpoints

Coverpoints define what values you want to track:

```python
# Add a coverpoint with discrete bins
cg.coverpoint("x", bins=[1, 2, 3, 4, 5])

# Add a coverpoint with range bins
cg.coverpoint("y", bins={"low": range(0, 10), "high": range(10, 20)})
```

## Registering a Covergroup

Before sampling values, you must register the covergroup:

```python
cg.register()
```

## Sampling Values

Use the `sample()` method to record values:

```python
cg.sample("x", 3)  # Record value 3 for coverpoint "x"
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
from pyfuncov import Covergroup

# Create and configure covergroup
cg = Covergroup("example")
cg.coverpoint("mode", bins=["read", "write", "idle"])
cg.coverpoint("address", bins={"low": range(0, 256), "high": range(256, 512)})

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
| `coverpoint(name, bins)` | Add a coverpoint with specified bins |
| `register()` | Register the covergroup before sampling |
| `sample(name, value)` | Record a sampled value |
| `report()` | Generate coverage report |
