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

This creates two bins (inclusive on both ends):
- `low`: values 0-256
- `high`: values 256-512

## Transition Bins

Transition bins track sequences of values (previous value -> current value):

```python
cg.add_coverpoint(
    name="state",
    bins=[
        Bin(name="idle_to_active", bin_type=BinKind.TRANSITION, from_value=0, to_value=1),
        Bin(name="active_to_idle", bin_type=BinKind.TRANSITION, from_value=1, to_value=0),
    ]
)
```

This tracks transitions from 0 to 1 and from 1 to 0. The covergroup automatically tracks the previous value when you call `sample()`.

## Complete Example

```python
from pyfuncov import Covergroup, Bin, BinKind, save_coverage, load_coverage, get_coverage_data, generate_report

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

# Save and generate report
save_coverage("coverage.json")
load_coverage("coverage.json")
data = get_coverage_data()
print(generate_report("text", {"covergroups": data.covergroups}))
```

## Bin Types Summary

| Type | Use Case |
|------|----------|
| DISCRETE | Track specific values |
| RANGE | Track values in ranges |
| TRANSITION | Track sequences of values |
