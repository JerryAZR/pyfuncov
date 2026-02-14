# Coverpoints

Coverpoints define what values to track within a covergroup. pyfuncov supports three types of bins: discrete, range, and transition.

## Discrete Bins

Discrete bins track specific individual values:

```python
from pyfuncov import Bin, BinKind

cg.add_coverpoint(
    name="x",
    bins=[
        Bin(name="one", bin_type=BinKind.DISCRETE, value=1),
        Bin(name="two", bin_type=BinKind.DISCRETE, value=2),
        Bin(name="three", bin_type=BinKind.DISCRETE, value=3),
    ]
)
```

This creates bins for values 1, 2, and 3.

## Range Bins

Range bins track values within a range:

```python
cg.add_coverpoint(
    name="address",
    bins=[
        Bin(name="low", bin_type=BinKind.RANGE, range_min=0, range_max=256),
        Bin(name="high", bin_type=BinKind.RANGE, range_min=256, range_max=512),
    ]
)
```

This creates two bins:
- `low`: values 0-255
- `high`: values 256-511

## Transition Bins

Transition bins track sequences of values:

```python
cg.add_coverpoint(
    name="state",
    bins=[
        Bin(name="idle_to_active", bin_type=BinKind.TRANSITION, value=["idle", "active"]),
        Bin(name="active_to_idle", bin_type=BinKind.TRANSITION, value=["active", "idle"]),
    ]
)
```

This tracks transitions from idle to active and vice versa.

## Complete Example

```python
from pyfuncov import Covergroup, Bin, BinKind

cg = Covergroup(name="coverage", module="test")

# Discrete bins
cg.add_coverpoint(
    name="opcode",
    bins=[
        Bin(name="op0", bin_type=BinKind.DISCRETE, value=0x00),
        Bin(name="op1", bin_type=BinKind.DISCRETE, value=0x01),
    ]
)

# Range bins
cg.add_coverpoint(
    name="address",
    bins=[
        Bin(name="kernel", bin_type=BinKind.RANGE, range_min=0, range_max=0x1000),
        Bin(name="user", bin_type=BinKind.RANGE, range_min=0x1000, range_max=0x10000),
    ]
)

cg.register()

# Sample values
cg.sample("opcode", 0x01)
cg.sample("address", 0x0500)  # Falls in "kernel" range

print(cg.report())
```

## Bin Types Summary

| Type | Use Case |
|------|----------|
| DISCRETE | Track specific values |
| RANGE | Track values in ranges |
| TRANSITION | Track sequences of values |
