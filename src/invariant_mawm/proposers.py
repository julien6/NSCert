"""Deterministic candidate proposer interfaces and enumeration.

The enumerator is deliberately grammar-agnostic: registries construct type-checked
objects, while this module provides stable traversal, deduplication, accounting, and
resumption without inspecting private feature metadata.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Iterable, Iterator, Protocol, Sequence

from .core import PartialInvariant, Precondition, Reading, RuleCandidate, Transport


class CandidateProposer(Protocol):
    name: str
    def propose(self) -> Iterator[RuleCandidate]: ...


@dataclass
class ProposalStatistics:
    predicted_count: int = 0
    visited_count: int = 0
    realized_count: int = 0
    duplicate_count: int = 0
    incompatible_count: int = 0
    resumed_count: int = 0
    by_memory_order: dict[int, int] = field(default_factory=dict)


def type_compatible(reading: Reading, transport: Transport) -> bool:
    """Check optional registry type annotations without guessing missing semantics."""
    reading_type = reading.parameters.get("value_type")
    supported = transport.parameters.get("supported_types")
    return supported is None or reading_type is None or reading_type in supported


class EnumerativeProposer:
    name = "P1"

    def __init__(self, readings: Sequence[Reading], preconditions: Sequence[Precondition],
                 transports: Sequence[Transport], memory_orders: Sequence[int], *,
                 seed: int = 0, resume_path: str | Path | None = None) -> None:
        self.readings = tuple(sorted(readings, key=lambda value: value.canonical))
        self.preconditions = tuple(sorted(preconditions, key=lambda value: json.dumps(asdict(value), sort_keys=True)))
        self.transports = tuple(sorted(transports, key=lambda value: json.dumps(asdict(value), sort_keys=True)))
        self.memory_orders = tuple(sorted(set(memory_orders)))
        if any(order < 0 for order in self.memory_orders): raise ValueError("memory orders must be nonnegative")
        self.seed = seed
        self.resume_path = Path(resume_path) if resume_path else None
        self.statistics = ProposalStatistics(
            predicted_count=len(self.readings)*len(self.preconditions)*len(self.transports)*len(self.memory_orders)
        )

    def _resumed_ids(self) -> set[str]:
        if self.resume_path is None or not self.resume_path.exists(): return set()
        ids=set()
        for line_number,line in enumerate(self.resume_path.read_text().splitlines(),1):
            try: ids.add(json.loads(line)["rule_id"])
            except (json.JSONDecodeError,KeyError) as exc:
                raise ValueError(f"invalid resume record at line {line_number}") from exc
        return ids

    def propose(self) -> Iterator[RuleCandidate]:
        resumed=self._resumed_ids(); seen=set(resumed)
        destination=self.resume_path.open("a") if self.resume_path else None
        try:
            for reading in self.readings:
                for precondition in self.preconditions:
                    for transport in self.transports:
                        for order in self.memory_orders:
                            self.statistics.visited_count += 1
                            if not type_compatible(reading,transport):
                                self.statistics.incompatible_count += 1; continue
                            invariant=PartialInvariant(reading,precondition,transport,order)
                            if invariant.rule_id in seen:
                                if invariant.rule_id in resumed: self.statistics.resumed_count += 1
                                else: self.statistics.duplicate_count += 1
                                continue
                            seen.add(invariant.rule_id)
                            candidate=RuleCandidate(invariant,self.name,self.seed)
                            self.statistics.realized_count += 1
                            self.statistics.by_memory_order[order]=self.statistics.by_memory_order.get(order,0)+1
                            if destination:
                                destination.write(json.dumps({"rule_id":invariant.rule_id},sort_keys=True)+"\n")
                                destination.flush()
                            yield candidate
        finally:
            if destination: destination.close()

