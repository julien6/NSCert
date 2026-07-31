"""Unpublished deterministic multi-agent benchmark for contamination controls."""
from __future__ import annotations
from dataclasses import dataclass
import random
from typing import Mapping

@dataclass(frozen=True)
class CounterWorldConfig:
    agents: int = 2
    lower: int = 0
    upper: int = 7
    cooldown_reset: int = 2
    horizon: int = 32

class CounterWorld:
    """Clipped positions plus reset/countdown dynamics with no semantic dependencies."""
    actions=(-1,0,1)
    version="1.0"
    def __init__(self, config:CounterWorldConfig=CounterWorldConfig()) -> None:
        if config.agents<1 or config.lower>=config.upper or config.horizon<1:
            raise ValueError("invalid CounterWorld configuration")
        self.config=config; self._rng=random.Random(); self._t=0
        self._positions=[config.lower]*config.agents; self._cooldowns=[0]*config.agents

    def reset(self, seed:int)->dict[str,int]:
        self._rng.seed(seed); self._t=0
        self._positions=[self._rng.randint(self.config.lower,self.config.upper) for _ in range(self.config.agents)]
        self._cooldowns=[self._rng.randint(0,self.config.cooldown_reset) for _ in range(self.config.agents)]
        return self.observation()

    def observation(self)->dict[str,int]:
        return {f"agent{i}.{name}": values[i] for i in range(self.config.agents)
                for name,values in (("position",self._positions),("cooldown",self._cooldowns))}

    def step(self, joint_action:Mapping[int,int])->tuple[dict[str,int],bool,dict]:
        if set(joint_action)!=set(range(self.config.agents)): raise ValueError("one action per agent is required")
        for i in range(self.config.agents):
            action=joint_action[i]
            if action not in self.actions: raise ValueError(f"invalid action {action}")
            self._positions[i]=min(self.config.upper,max(self.config.lower,self._positions[i]+action))
            self._cooldowns[i]=self.config.cooldown_reset if action else max(0,self._cooldowns[i]-1)
        self._t+=1
        return self.observation(),self._t>=self.config.horizon,{"timestep":self._t}

    @staticmethod
    def oracle_rule_families()->tuple[str,...]:
        """Evaluation-only labels; collection and proposers never call this method."""
        return ("clipped_action_offset","action_reset","zero_action_countdown")
