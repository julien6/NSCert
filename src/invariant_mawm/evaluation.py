"""Evaluate fitted scalar affine rules on transition records."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from .data import Transition
from .transports import bounded_affine

@dataclass(frozen=True)
class RuleEvaluation:
    total_transitions:int
    conditional_support:int
    violations:int
    tolerance:float
    @property
    def violation_rate(self)->float: return self.violations/self.conditional_support if self.conditional_support else 0.0

def evaluate_affine(records:Iterable[Transition], *, feature:str, agent:int,
                    alpha:float, offsets:dict[int,float], lower:float, upper:float,
                    action_equals:int|None=None, tolerance:float=0.0)->RuleEvaluation:
    if tolerance<0: raise ValueError("tolerance must be nonnegative")
    total=support=violations=0
    for record in records:
        total+=1; action=record.joint_action[agent]
        if action_equals is not None and action!=action_equals: continue
        support+=1
        predicted=bounded_affine(record.joint_observation[feature],action,alpha=alpha,
                                  offsets=offsets,lower=lower,upper=upper)
        if abs(record.next_joint_observation[feature]-predicted)>tolerance: violations+=1
    return RuleEvaluation(total,support,violations,tolerance)
