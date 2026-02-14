# Coverpoints

Coverpoints define what values to track within a covergroup. pyfuncov supports three types of bins: discrete, range, and transition.

## Discrete Bins

Discrete bins track specific individual values:

```python
cg.coverpoint("x", bins=[1, 2, 3, 4, 5])
```

This creates bins for values 1, 2, 3, 4, and 5.

## Range Bins

Range bins track values within a range:

```python
cg.coverpoint("address", bins={
    "low": range(0, 256),
    "high": range(256, 512)
})
```

This creates two bins:
- `low`: values 0-255
- `high`: values 256-511

## Transition Bins

Transition bins track sequences of values:

```python
cg.coverpoint("state", bins={
    "idle_to_active": ["idle", "active"],
    "active_to_idle": ["active", "idle"]
})
```

This tracks transitions from idle to active and vice versa.

## Bin Options

You can combine different bin types:

```python
cg.coverpoint("mixed", bins=[
    1, 2, 3,           # Discrete bins
    {"small": range(0, 10)},  # Range bin
    {"valid": [1, 2, 3, 4, 5]}  # Valid values
])
```

## Auto-bins

Let pyfuncov automatically create bins:

```python
cg.coverpoint("auto", bins=10)  # Creates 10 equal-width bins
```

## Complete Example

```python
from pyfuncov import Covergroup

cg = Covergroup("coverage")

# Discrete bins
cg.coverpoint("opcode", bins=[0x00, 0x01, 0x02, 0x03])

# Range bins
cg.coverpoint("address", bins={
    "kernel": range(0, 0x1000),
    "user": range(0x1000, 0x10000)
})

# Transition bins
cg.coverpoint("state", bins={
    "transitions": ["init", "running", "done", "init"]
})

cg.register()

# Sample values
cg.sample("opcode", 0x01)
cg.sample("address", 0x0500)  # Falls in "kernel" range
cg.sample("state", "init")
cg.sample("state", "running")
cg.sample("state", "done")

print(cg.report())
```

## Bin Types Summary

| Type | Use Case |
|------|----------|
| Discrete | Track specific values |
| Range | Track values in ranges |
| Transition | Track sequences of values |
| Auto | Automatically divide range into bins |
