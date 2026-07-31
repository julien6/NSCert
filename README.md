# NSCert

An auditable, from-scratch reconstruction scaffold for partial symbolic invariants in
neuro-symbolic multi-agent world models. The current release implements the formal
objects, readings, bounded preconditions, core transports, leakage checks, statistical
certification, and promotion policy. It does **not** claim reproduced paper results.

## Quick start

```bash
python -m pip install -e '.[dev]'
pytest
invariant-mawm --support 300 --candidates 100
PYTHONPATH=src python scripts/collect/collect_synthetic.py --output /tmp/nscert-data
PYTHONPATH=src python scripts/analyze/generate_transport_catalog.py
```

Published values belong only in `references/paper_reported_results.yaml`; generated
outputs must be derived from runs. See `docs/reproduction_status.md` for current scope
and `docs/paper_traceability.md` for specification provenance.
## Reproducibility

Use seeds `0 1 2 3 4`. Each run must retain its Git commit, config, seed, environment
versions, dataset manifest, command, and W&B run ID. W&B may run offline via
`WANDB_MODE=offline`. Large datasets and checkpoints are intentionally ignored.
