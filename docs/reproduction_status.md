# Reproduction status

This is a tested foundation, **not a completed scientific reproduction**. Implemented:
typed serialization, canonical IDs, reading evaluation/anonymization, bounded ASTs and
auditable non-vacuity checks, three transport primitives, content- and episode-level
split-leakage checks, numerically stable IID bounds, effective-budget accounting,
validated rule inventories with optional W&B Table export, and promotion thresholds. Proposers, full environments,
active gates, anytime-valid inference, MAWM training/injection, W&B artifact workflows,
and paper tables/figures remain pending because the authoritative paper was unavailable.

The deterministic P1 enumeration foundation now provides type pruning, canonical
ordering, duplicate accounting, and JSONL resumption. The F1--F4 gate ladder provides
disjoint-dataset enforcement and per-gate finite-sample evidence summaries. Immutable
dataset manifests capture collection provenance and payload checksums. Environment
adapters and the active policies needed to populate those gates remain future work.

An unpublished CounterWorld environment now exercises multi-agent clipped motion,
action resets, and countdown dynamics. Its deterministic collector produces disjoint
smoke partitions, and the integration pipeline certifies an evaluation-only oracle
motion rule. This is a contamination-control benchmark, not a substitute for the paper
environments or their reported experiments.

Certification now includes an anytime-valid error-spending sequence over conservative
episode-level violation indicators. Rule lifecycle support covers soft/hard injection
decisions, immediate hard-rule retrogradation, at-risk denominators, fresh-evidence
requirements, stricter re-promotion, and `R_max` caps. Neural model training remains
pending; injection decisions currently expose the contract a trainer must apply.
