# Synthetic contamination-control benchmark

CounterWorld supplies a paper-independent validation target. It is deterministic given
the environment seed, has multi-agent joint actions, clipped motion, action-conditioned
resets, and countdown dynamics. Partition collection uses disjoint episode identifiers
and independent policy RNG streams. The oracle catalog is stored separately for
evaluation and is not imported by the environment collector or proposer modules.
