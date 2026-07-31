"""Permutation-safe reading evaluation and feature anonymization."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib, json, random
from typing import Any, Mapping, Sequence
from .core import Reading

def evaluate(r: Reading, obs: dict[str, Any]) -> Any:
    xs=[obs[f] for f in r.features]; k=r.kind
    if k in {"scalar","categorical","indicator"}: return xs[0]
    if k=="equality": return xs[0]==xs[1]
    if k=="inequality": return xs[0]!=xs[1]
    if k=="difference": return xs[0]-xs[1]
    if k=="distance": return abs(xs[0]-xs[1])
    if k=="ordering": return xs[0]<xs[1]
    if k=="cooccurrence": return bool(xs[0]) and bool(xs[1])
    if k=="count": return sum(bool(x) for x in xs)
    if k=="sum": return sum(xs)
    if k=="mean": return sum(xs)/len(xs)
    if k=="min": return min(xs)
    if k=="max": return max(xs)
    if k=="any": return any(xs)
    if k=="all": return all(xs)
    raise ValueError(f"unknown reading kind {k}")

REGISTRY=frozenset({"scalar","categorical","indicator","equality","inequality","difference",
 "distance","ordering","cooccurrence","count","sum","mean","min","max","any","all"})

@dataclass(frozen=True)
class Anonymization:
    public: dict[str,str]
    private_reverse: dict[str,str]
    mapping_hash: str
    slot_public: dict[str,str] = None
    scales: dict[str,tuple[float,float,float,float]] = None

    def transform(self, observation: Mapping[str,Any])->dict[str,Any]:
        result={}
        for name,value in observation.items():
            public=self.public[name]
            if self.scales and name in self.scales:
                old_lo,old_hi,new_lo,new_hi=self.scales[name]
                value=new_lo+(value-old_lo)*(new_hi-new_lo)/(old_hi-old_lo)
            result[public]=value
        return result

    def reverse(self, observation: Mapping[str,Any])->dict[str,Any]:
        result={}
        for public,value in observation.items():
            name=self.private_reverse[public]
            if self.scales and name in self.scales:
                old_lo,old_hi,new_lo,new_hi=self.scales[name]
                value=old_lo+(value-new_lo)*(old_hi-old_lo)/(new_hi-new_lo)
            result[name]=value
        return result

def anonymize(features: Sequence[str], seed: int, permute_slots: bool=False,
              agent_slots:Sequence[str]|None=None,
              value_ranges:Mapping[str,tuple[float,float]]|None=None,
              rescale:bool=False) -> Anonymization:
    if len(set(features)) != len(features): raise ValueError("feature identifiers must be unique")
    ordered=list(features); random.Random(seed).shuffle(ordered)
    public={original:f"f{i:04d}" for i,original in enumerate(ordered)}
    reverse={v:k for k,v in public.items()}
    slots=list(agent_slots or ()); rng=random.Random(seed+1)
    if permute_slots: rng.shuffle(slots)
    slot_public={original:f"a{i:03d}" for i,original in enumerate(slots)}
    scales={}
    if rescale:
        if not value_ranges: raise ValueError("value_ranges are required for rescaling")
        for i,name in enumerate(sorted(value_ranges)):
            lo,hi=value_ranges[name]
            if hi<=lo: raise ValueError("value ranges must be increasing")
            new_lo=float(i*2-1); scales[name]=(lo,hi,new_lo,new_lo+1.0)
    payload={"features":public,"slots":slot_public,"scales":scales}
    digest=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    return Anonymization(public,reverse,digest,slot_public,scales)
