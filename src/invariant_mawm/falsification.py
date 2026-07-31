"""Sequential F1--F4 evidence accounting and certification."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable

from .certification import clopper_pearson_upper, zero_violation_bound
from .core import GateResult

GATE_ORDER=("F1","F2","F3","F4")

@dataclass(frozen=True)
class GateEvidence:
    gate: str
    total_transitions: int
    conditional_support: int
    violations: int
    dataset_ids: tuple[str,...]
    metadata: dict = field(default_factory=dict)

    def validate(self) -> None:
        if self.gate not in GATE_ORDER: raise ValueError(f"unknown gate {self.gate}")
        if not 0 <= self.violations <= self.conditional_support <= self.total_transitions:
            raise ValueError("require violations <= support <= total transitions")
        if not self.dataset_ids: raise ValueError("gate evidence requires dataset provenance")


@dataclass(frozen=True)
class GateLadderResult:
    results: tuple[GateResult,...]
    stopped_after: str | None


def run_gate_ladder(evidence: Iterable[GateEvidence], *, delta: float=.05,
                    maximum_violation_rate: float=.01, budget: int=1) -> GateLadderResult:
    if not 0 <= maximum_violation_rate <= 1: raise ValueError("maximum violation rate must be in [0, 1]")
    items=list(evidence)
    if [item.gate for item in items] != list(GATE_ORDER[:len(items)]):
        raise ValueError("gate evidence must be an F1-to-F4 prefix")
    used_datasets:set[str]=set(); results=[]; stopped=None
    for item in items:
        item.validate()
        overlap=used_datasets.intersection(item.dataset_ids)
        if overlap: raise ValueError(f"datasets reused across gates: {sorted(overlap)}")
        used_datasets.update(item.dataset_ids)
        if item.violations == 0:
            upper=zero_violation_bound(item.conditional_support,delta,budget)
        elif item.conditional_support:
            upper=clopper_pearson_upper(item.violations,item.conditional_support,delta/budget)
        else: upper=1.0
        passed=upper <= maximum_violation_rate
        results.append(GateResult(item.gate,item.conditional_support,
            item.conditional_support/item.total_transitions if item.total_transitions else 0.0,
            item.violations,item.violations/item.conditional_support if item.conditional_support else 0.0,
            upper,passed))
        if not passed: stopped=item.gate; break
    return GateLadderResult(tuple(results),stopped)
