# CounterWorld synthetic benchmark

CounterWorld is an unpublished deterministic multi-agent environment intended for
contamination-control and end-to-end smoke tests. Each agent selects `-1`, `0`, or `1`.
Positions follow clipped action offsets. A nonzero action resets cooldown to two; a zero
action decrements cooldown to zero. Oracle family names are evaluation-only and must not
be supplied to candidate proposers.
