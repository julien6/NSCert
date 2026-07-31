"""Canonical bounded-depth precondition AST."""
from dataclasses import dataclass, field
from typing import Any, Iterator
from .core import Precondition, canonical

def depth(p: Precondition) -> int:
    children=[x for x in p.operands if isinstance(x,Precondition)]
    return 1+(max(map(depth,children)) if children else 0)

def validate(p: Precondition, beta: int=2) -> None:
    allowed={"eq","ne","lt","le","gt","ge","interval","action","joint_action","and","or"}
    if p.operator not in allowed: raise ValueError(p.operator)
    if depth(p)>beta: raise ValueError(f"precondition depth exceeds beta={beta}")

def canonicalize(p: Precondition) -> str:
    operands=p.operands
    if p.operator in {"and","or","eq","ne"}: operands=tuple(sorted(operands,key=canonical))
    return canonical(Precondition(p.operator,operands))

@dataclass(frozen=True)
class ScreenResult:
    reasons: tuple[str,...]
    support: int
    total: int
    diagnostics: dict[str,Any]=field(default_factory=dict)
    def __iter__(self)->Iterator[str]: return iter(self.reasons)
    def __contains__(self,item:object)->bool: return item in self.reasons

def screen(values: list[Any], fires: list[bool], targets: list[Any], *, pi_min=.01,
           n_min=300, action_branches:dict[str,int]|None=None,
           split:str|None=None) -> ScreenResult:
    if not (len(values)==len(fires)==len(targets)):
        raise ValueError("values, fires, and targets must have equal lengths")
    if not 0<=pi_min<=1 or n_min<0: raise ValueError("invalid screening threshold")
    reasons=[]; n=sum(fires); total=len(fires)
    if len(set(values))<=1: reasons.append("constant_reading")
    if total==0 or n/total < pi_min: reasons.append("rare_precondition")
    if n<n_min: reasons.append("insufficient_conditional_support")
    selected=[t for t,f in zip(targets,fires) if f]
    if selected and len(set(selected))<=1: reasons.append("target_never_changes")
    if any(v is None for v in values): reasons.append("missing_value_padding")
    if action_branches and any(count<n_min for count in action_branches.values()):
        reasons.append("inadequate_action_branch_support")
    if split in {"Dtest","Dshift"}: reasons.append("prohibited_split_leakage")
    return ScreenResult(tuple(reasons),n,total,{"trigger_frequency": n/total if total else 0.0})
