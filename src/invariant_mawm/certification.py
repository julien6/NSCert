"""Finite-sample certification utilities (standard-library implementation)."""
import math
from dataclasses import dataclass

def effective_budget(m_hat:int, soft:int=3, hard:int=3, m_max:int=4, beta_grid:int=1, k:int=4, r_max:int=2)->int:
    values=(m_hat,soft,hard,beta_grid,k,r_max)
    if any(v<=0 for v in values) or m_max<0: raise ValueError("budget factors must be positive")
    return m_hat*soft*hard*(m_max+1)*beta_grid*k*r_max

def zero_violation_bound(n:int, delta:float=.05, budget:int=1)->float:
    if not 0<delta<1 or budget<=0 or n<0: raise ValueError("invalid confidence parameters")
    if n<=0: return 1.0
    return min(1.0, math.log(budget/delta)/n)

def clopper_pearson_upper(violations:int,n:int,delta:float=.05)->float:
    """One-sided exact binomial upper endpoint, found by bisection."""
    if not 0<delta<1: raise ValueError("delta must be in (0, 1)")
    if not 0<=violations<=n or n==0: raise ValueError("require 0 <= violations <= n and n > 0")
    if violations==n: return 1.0
    lo,hi=violations/n,1.0
    # Solve P_p[X <= k] = delta; monotone decreasing in p.
    for _ in range(80):
        p=(lo+hi)/2
        logs=[math.lgamma(n+1)-math.lgamma(i+1)-math.lgamma(n-i+1)
              + i*math.log(p) + (n-i)*math.log1p(-p)
              for i in range(violations+1)]
        peak=max(logs); cdf=math.exp(peak)*sum(math.exp(x-peak) for x in logs)
        if cdf>delta: lo=p
        else: hi=p
    return hi

def promote(q:float, soft:float=.90, hard:float=.99)->str:
    if not 0<=q<=1: raise ValueError("q must be a probability")
    return "REJECTED" if q<soft else "SOFT" if q<hard else "HARD"

@dataclass(frozen=True)
class ConfidenceSequencePoint:
    support:int
    violations:int
    upper_bound:float
    allocated_delta:float

class AnytimeBernoulliCS:
    """Anytime-valid IID Bernoulli upper sequence via summable error spending.

    At time n, delta/(n(n+1)) is assigned to a one-sided Clopper--Pearson
    interval. Since the allocations sum to delta, a union bound gives simultaneous
    coverage at every n and therefore permits adaptive stopping. For dependent
    transitions, callers must first construct episode-level Bernoulli observations.
    """
    def __init__(self,delta:float=.05)->None:
        if not 0<delta<1: raise ValueError("delta must be in (0, 1)")
        self.delta=delta; self.support=0; self.violations=0
    def update(self,violation:bool)->ConfidenceSequencePoint:
        self.support+=1; self.violations+=int(violation)
        allocation=self.delta/(self.support*(self.support+1))
        upper=clopper_pearson_upper(self.violations,self.support,allocation)
        return ConfidenceSequencePoint(self.support,self.violations,upper,allocation)
    def update_episode(self,transition_violations:list[bool])->ConfidenceSequencePoint:
        """Retain one conservative relevant outcome: any violation in an episode."""
        if not transition_violations: raise ValueError("episode has no relevant transitions")
        return self.update(any(transition_violations))
