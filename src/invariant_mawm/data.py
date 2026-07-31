"""Immutable manifest and leakage checks."""
from dataclasses import dataclass
import hashlib, json
from typing import Iterable

@dataclass(frozen=True)
class Transition:
    dataset_id:str; environment_id:str; environment_version:str; variant_id:str
    generator_id:str; policy_id:str; episode_id:str; timestep:int; seed:int
    joint_observation:dict; joint_action:object; next_joint_observation:dict
    history_reference:str|None=None; termination:bool=False; truncation:bool=False
    latent_state:dict|None=None; metadata:dict|None=None
    def episode_identity(self)->tuple[str,...]:
        return (self.environment_id,self.environment_version,self.variant_id,
                self.generator_id,self.episode_id)
    def fingerprint(self)->str:
        """Content identity independent of split-local episode numbering."""
        payload=(self.environment_id,self.environment_version,self.variant_id,
                 self.seed,
                 self.joint_observation,self.joint_action,self.next_joint_observation,
                 self.termination,self.truncation)
        return hashlib.sha256(json.dumps(payload,sort_keys=True,default=str).encode()).hexdigest()

def assert_disjoint(splits:dict[str,Iterable[Transition]])->None:
    episodes:dict[tuple[str,...],str]={}; fingerprints:dict[str,str]={}
    for split, records in splits.items():
        for r in records:
            episode=r.episode_identity()
            if episode in episodes and episodes[episode]!=split: raise ValueError("episode leakage")
            episodes[episode]=split
            fp=r.fingerprint()
            if fp in fingerprints and fingerprints[fp]!=split: raise ValueError("transition leakage")
            fingerprints[fp]=split
