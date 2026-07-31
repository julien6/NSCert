"""Deterministic transport catalog."""
from __future__ import annotations
from itertools import permutations
import math
from typing import Iterable, Sequence

def bounded_affine(phi: float, action: str, *, alpha: float, offsets: dict[str,float], lower: float, upper: float) -> float:
    return min(upper,max(lower,alpha*phi+offsets.get(action,0.0)))

def fit_affine(xs: Iterable[float], ys: Iterable[float], actions: Iterable[str], alphas=(0.0,1.0)) -> dict:
    xs,ys,actions=list(xs),list(ys),list(actions)
    if not xs or not (len(xs)==len(ys)==len(actions)): raise ValueError("aligned nonempty samples required")
    if any(not math.isfinite(float(v)) for v in xs+ys): raise ValueError("samples must be finite")
    best=None
    for alpha in alphas:
        offsets={}
        for action in sorted(set(actions)):
            residuals=[y-alpha*x for x,y,a in zip(xs,ys,actions) if a==action]
            candidates=sorted(set(residuals+[sum(residuals)/len(residuals)]))
            offsets[action]=min(candidates,key=lambda d:(sum((y-min(max(alpha*x+d,min(ys)),max(ys)))**2
                for x,y,a in zip(xs,ys,actions) if a==action),d))
        error=sum((y-bounded_affine(x,a,alpha=alpha,offsets=offsets,lower=min(ys),upper=max(ys)))**2
                  for x,y,a in zip(xs,ys,actions))
        candidate=(error,alpha,offsets)
        if best is None or (candidate[0],candidate[1])<(best[0],best[1]): best=candidate
    return {"alpha":best[1],"offsets":best[2],"lower":min(ys),"upper":max(ys),
            "sample_count":len(xs),"objective":best[0],
            "action_support":{a:actions.count(a) for a in sorted(set(actions))}}

def delayed_copy(history: Sequence[object], m: int) -> object:
    if m<0 or m>=len(history): raise IndexError(m)
    return history[-1-m]

def infer_permutation(source: Sequence[object], target: Sequence[object]) -> tuple[int,...]:
    if len(source)!=len(target): raise ValueError("slot counts differ")
    matches=[p for p in permutations(range(len(source))) if tuple(source[i] for i in p)==tuple(target)]
    if not matches: raise ValueError("no exact assignment")
    return min(matches)
