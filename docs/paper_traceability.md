# Paper-to-artifact traceability

> **Availability warning.** No paper PDF, appendix, DOI, or bibliographic record was
> present in the supplied repository. An exact-title web lookup was attempted but the
> configured search service returned HTTP 401. Therefore this initial inventory is
> derived exclusively from the supplied master prompt; paper-dependent claims remain
> `UNRESOLVED` rather than being silently invented.

| ID | Paper section | Paper claim/specification | Artifact implementation | Status | Confidence | Notes |
|---|---|---|---|---|---|---|
| F-01 | Formalism | Rule is `(reading, precondition, transport)` with conditional violations | `core.PartialInvariant` | RECONSTRUCTED_FROM_CONTEXT | High | Prompt specification |
| F-02 | Readings | Atomic, pairwise, and per-agent aggregates; permutation safe | `readings.py` registry/evaluator | RECONSTRUCTED_FROM_CONTEXT | Medium | Masked and agent-relative registry expansion remains |
| F-03 | Transport | Bounded affine with action offsets and clipping | `transports.bounded_affine`, `fit_affine` | RECONSTRUCTED_FROM_CONTEXT | High | Discrete tolerance policy unresolved |
| F-04 | Transport | Delayed copy through memory four | `transports.delayed_copy`; config | RECONSTRUCTED_FROM_CONTEXT | High | Cross-feature compatibility belongs in proposer |
| F-05 | Transport | Agent-slot permutation and assignment | `transports.infer_permutation` | RECONSTRUCTED_FROM_CONTEXT | Medium | Exact factorial solver; scalable Hungarian extension pending |
| F-06 | Preconditions | Bounded canonical AST, default depth two | `preconditions.py` | RECONSTRUCTED_FROM_CONTEXT | High | Restricted disjunction supported syntactically |
| F-07 | Screening | Non-vacuity, frequency .01, support 300 | `preconditions.screen` | RECONSTRUCTED_FROM_CONTEXT | Medium | Encoding/leakage screens require schema context |
| F-08 | Proposers | Enumerative, decision-tree, provider-independent LLM | Deterministic typed P1 foundation in `proposers.py`; P2/P3 pending | RECONSTRUCTED_FROM_CONTEXT | Medium | Paper algorithm and prompts unavailable |
| F-09 | Data | Four disjoint partitions 60k/40k/40k/20k | config and `data.assert_disjoint` | RECONSTRUCTED_FROM_CONTEXT | High | Collection environments unavailable |
| F-10 | Gates | Sequential F1 passive, F2 active, F3 variant, F4 generator | Evidence/certification ladder in `falsification.py`; collectors pending | RECONSTRUCTED_FROM_CONTEXT | Medium | Exploration details unspecified by paper text |
| F-11 | Statistics | IID zero-event union bound, Clopper–Pearson, and anytime validity | IID bounds plus episode-level error-spending confidence sequence in `certification.py` | RECONSTRUCTED_FROM_CONTEXT | Medium | Auditable reconstruction; authoritative paper reference remains unavailable |
| F-12 | Budget | Candidate/grid/memory/beta × K × Rmax | `effective_budget` | RECONSTRUCTED_FROM_CONTEXT | High | Meaning of candidate estimate needs paper |
| F-13 | Promotion | reject/soft/hard at .90/.99; retrogradation | Lifecycle, injection decisions, immediate retrogradation, fresh-data re-promotion cap in `injection.py` | RECONSTRUCTED_FROM_CONTEXT | Medium | Definition of q remains unresolved |
| F-14 | MAWM | GRU-256, 2×256 encoder/decoder, Adam defaults | configuration only | RECONSTRUCTED_FROM_CONTEXT | High | Detailed loss and injection equations unavailable |
| E-01 | Environments | GridCraft, Overcooked, Predator–Prey, SMACv2, synthetic | Unpublished CounterWorld smoke benchmark implemented; paper environments pending | EXTENSION_BEYOND_PAPER | High | Versions, tasks, schemas, and oracle rules for paper environments unavailable |
| E-02 | Experiments | All tables, figures, ablations, diagnostics | Not generated | UNRESOLVED | Low | Paper/appendix required to enumerate them |
| C-01 | Compute | Local, Docker, DGX Spark support | Docker scaffold | REASONABLE_DEFAULT | Medium | Paper computational claims unavailable |
| L-01 | Limitations | contamination controls and no semantic leakage | anonymization primitive | RECONSTRUCTED_FROM_CONTEXT | Medium | LLM proposer pending |
| X-01 | Extension | Unpublished synthetic contamination control | `environments/synthetic.py`, collector, separated oracle file, integration test | EXTENSION_BEYOND_PAPER | High | No paper result is claimed |

## Unavailable items requiring the authoritative paper

Definitions/equations beyond the prompt, algorithms, propositions, theorems and proofs,
environment versions, dataset provenance, baseline definitions, exact hyperparameters,
all reported values, table/figure layouts, appendix references, limitations, contamination
claims, and computational claims are deliberately marked unresolved.
