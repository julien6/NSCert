"""Strongly typed, deterministic, serializable research objects."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


def canonical(value: Any) -> str:
    """Return a stable JSON representation used for IDs and deduplication."""
    if hasattr(value, "to_dict"):
        value = value.to_dict()
    elif hasattr(value, "__dataclass_fields__"):
        value = asdict(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


class PromotionStatus(StrEnum):
    REJECTED = "REJECTED"
    SOFT = "SOFT"
    HARD = "HARD"
    RETROGRADED = "RETROGRADED"
    PENDING_REPROMOTION = "PENDING_REPROMOTION"
    NON_CERTIFIABLE = "NON_CERTIFIABLE"


@dataclass(frozen=True)
class Reading:
    kind: str
    features: tuple[str, ...]
    parameters: Mapping[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]: return asdict(self)
    @property
    def canonical(self) -> str: return canonical(self)


@dataclass(frozen=True)
class Precondition:
    operator: str
    operands: tuple[Any, ...]
    def to_dict(self) -> dict[str, Any]: return asdict(self)


@dataclass(frozen=True)
class Transport:
    family: str
    parameters: Mapping[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]: return asdict(self)


@dataclass(frozen=True)
class PartialInvariant:
    reading: Reading
    precondition: Precondition
    transport: Transport
    memory_order: int = 0
    @property
    def rule_id(self) -> str:
        return hashlib.sha256(canonical(asdict(self)).encode()).hexdigest()[:16]
    def to_dict(self) -> dict[str, Any]: return asdict(self) | {"rule_id": self.rule_id}


@dataclass
class GateResult:
    gate: str
    conditional_support: int
    trigger_frequency: float
    violations: int
    empirical_violation_rate: float
    upper_bound: float
    passed: bool


@dataclass
class CertificationResult:
    method: str
    delta: float
    upper_bound: float
    effective_budget: int
    support: int
    violations: int


@dataclass
class RuleCandidate:
    invariant: PartialInvariant
    source_proposer: str
    proposal_seed: int


@dataclass
class FittedRule:
    candidate: RuleCandidate
    fit_dataset_id: str
    transport_parameters: Mapping[str, Any]


@dataclass
class DiscoveredMask:
    feature_ids: tuple[str, ...]
    source_rule_ids: tuple[str, ...]


@dataclass
class RuleInventory:
    rules: list[dict[str, Any]] = field(default_factory=list)
    def add(self, rule: Mapping[str, Any]) -> None:
        required = {"rule_id", "reading", "precondition", "transport", "memory_order",
                    "source_proposer", "proposal_seed", "fit_dataset_id", "gate_results",
                    "empirical_violation_rate", "confidence_or_validity_score",
                    "certificate_upper_bound", "conditional_support", "trigger_frequency",
                    "feature_coverage", "transition_coverage", "promotion_status",
                    "retrogradation_history", "reproduction_metadata"}
        missing = required - rule.keys()
        if missing: raise ValueError(f"missing rule fields: {sorted(missing)}")
        if rule["promotion_status"] not in {s.value for s in PromotionStatus}:
            raise ValueError("invalid promotion_status")
        gates=rule["gate_results"]
        if not isinstance(gates,Mapping) or any(g not in gates for g in ("F1","F2","F3","F4")):
            raise ValueError("gate_results must contain F1 through F4")
        for key in ("empirical_violation_rate","confidence_or_validity_score",
                    "certificate_upper_bound","trigger_frequency","feature_coverage",
                    "transition_coverage"):
            if not 0 <= float(rule[key]) <= 1: raise ValueError(f"{key} must be in [0, 1]")
        if int(rule["conditional_support"]) < 0: raise ValueError("support must be nonnegative")
        canonical(rule)  # fail early if the complete record cannot be serialized
        self.rules.append(dict(rule))
    def export_json(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.rules, indent=2, sort_keys=True, default=str)+"\n")
    def export_yaml(self, path: str | Path) -> None:
        import yaml
        Path(path).write_text(yaml.safe_dump(self.rules, sort_keys=True))
    def export_csv(self, path: str | Path) -> None:
        keys = sorted({k for r in self.rules for k in r})
        with Path(path).open("w", newline="") as f:
            w=csv.DictWriter(f, keys); w.writeheader()
            for row in self.rules: w.writerow({k: canonical(v) if isinstance(v,(dict,list)) else v for k,v in row.items()})
    def to_wandb_table(self) -> Any:
        """Create a W&B Table while keeping tracking an optional dependency."""
        try:
            import wandb
        except ImportError as exc:
            raise RuntimeError("install invariant-mawm[tracking] for W&B export") from exc
        keys=sorted({k for r in self.rules for k in r})
        rows=[[canonical(r.get(k)) if isinstance(r.get(k),(dict,list,tuple)) else r.get(k)
               for k in keys] for r in self.rules]
        return wandb.Table(columns=keys,data=rows)
