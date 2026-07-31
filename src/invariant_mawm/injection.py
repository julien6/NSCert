"""Rule promotion, injection decisions, retrogradation, and re-promotion controls."""
from __future__ import annotations
from dataclasses import dataclass, field
from .core import PromotionStatus

@dataclass
class ManagedRule:
    rule_id:str
    status:PromotionStatus=PromotionStatus.REJECTED
    promotion_score:float=0.0
    repromotion_attempts:int=0
    evidence_dataset_ids:set[str]=field(default_factory=set)
    retrogradation_history:list[dict]=field(default_factory=list)
    at_risk_transitions:int=0
    counterexamples:int=0

    def observe(self, *, violated:bool, dataset_id:str, timestep:int)->None:
        if self.status not in {PromotionStatus.SOFT,PromotionStatus.HARD}: return
        self.at_risk_transitions+=1
        if not violated: return
        self.counterexamples+=1
        if self.status is PromotionStatus.HARD:
            self.status=PromotionStatus.RETROGRADED
            self.retrogradation_history.append({"dataset_id":dataset_id,"timestep":timestep,
                "at_risk_transitions":self.at_risk_transitions})

    @property
    def retrogradation_rate(self)->float:
        return len(self.retrogradation_history)/self.at_risk_transitions if self.at_risk_transitions else 0.0

class RuleLifecycle:
    def __init__(self, *, tau_soft:float=.90,tau_hard:float=.99,
                 repromotion_tau:float=.995,r_max:int=2)->None:
        if not 0<=tau_soft<=tau_hard<=repromotion_tau<=1 or r_max<0:
            raise ValueError("invalid lifecycle thresholds")
        self.tau_soft=tau_soft; self.tau_hard=tau_hard
        self.repromotion_tau=repromotion_tau; self.r_max=r_max

    def promote(self,rule:ManagedRule,score:float,dataset_ids:set[str])->PromotionStatus:
        if not 0<=score<=1 or not dataset_ids: raise ValueError("promotion requires scored evidence")
        if rule.evidence_dataset_ids.intersection(dataset_ids):
            raise ValueError("promotion evidence must be disjoint")
        threshold=self.repromotion_tau if rule.status in {PromotionStatus.RETROGRADED,PromotionStatus.PENDING_REPROMOTION} else None
        if threshold is not None:
            if rule.repromotion_attempts>=self.r_max:
                rule.status=PromotionStatus.NON_CERTIFIABLE; return rule.status
            rule.repromotion_attempts+=1
        rule.evidence_dataset_ids.update(dataset_ids); rule.promotion_score=score
        if threshold is not None and score<threshold:
            rule.status=PromotionStatus.PENDING_REPROMOTION
        elif score>=self.tau_hard: rule.status=PromotionStatus.HARD
        elif score>=self.tau_soft: rule.status=PromotionStatus.SOFT
        else: rule.status=PromotionStatus.REJECTED
        return rule.status

@dataclass(frozen=True)
class InjectionDecision:
    neural_target:bool
    symbolic_prediction:float|None
    soft_penalty_weight:float

def injection_decision(rule:ManagedRule,symbolic_prediction:float,*,soft_weight:float=1.0)->InjectionDecision:
    if soft_weight<0: raise ValueError("soft weight must be nonnegative")
    if rule.status is PromotionStatus.HARD:
        return InjectionDecision(False,symbolic_prediction,0.0)
    if rule.status is PromotionStatus.SOFT:
        return InjectionDecision(True,None,soft_weight)
    return InjectionDecision(True,None,0.0)
