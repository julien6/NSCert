"""Deterministic transition collection with episode-disjoint partitions."""
from __future__ import annotations
from dataclasses import dataclass
import random
from typing import Callable, Mapping

from .data import Transition, assert_disjoint
from .environments.synthetic import CounterWorld

Policy=Callable[[dict[str,int],random.Random,int],Mapping[int,int]]

def random_policy(observation:dict[str,int], rng:random.Random, agents:int)->dict[int,int]:
    del observation
    return {i:rng.choice(CounterWorld.actions) for i in range(agents)}

def collect_episodes(env:CounterWorld, *, dataset_id:str, split:str, episodes:int,
                     seed:int, policy:Policy=random_policy, policy_id:str="random",
                     generator_id:str="builtin") -> list[Transition]:
    if episodes<0: raise ValueError("episodes must be nonnegative")
    records=[]; policy_rng=random.Random(seed)
    for episode_index in range(episodes):
        episode_seed=seed+episode_index
        observation=env.reset(episode_seed); done=False; timestep=0
        episode_id=f"{split}-{seed}-{episode_index}"
        while not done:
            action=dict(policy(observation,policy_rng,env.config.agents))
            next_observation,done,metadata=env.step(action)
            records.append(Transition(dataset_id,"counter_world",env.version,"base",
                generator_id,policy_id,episode_id,timestep,episode_seed,dict(observation),action,
                dict(next_observation),termination=done,metadata=metadata | {"split":split}))
            observation=next_observation; timestep+=1
    return records

def collect_partitions(env_factory:Callable[[],CounterWorld], sizes:Mapping[str,int], *, seed:int=0)->dict[str,list[Transition]]:
    split_order=("Dprop","Dfit","Dtest","Dshift")
    unknown=set(sizes)-set(split_order)
    if unknown: raise ValueError(f"unknown partitions: {sorted(unknown)}")
    partitions={split:collect_episodes(env_factory(),dataset_id=f"counter-{split}-{seed}",
                    split=split,episodes=count,seed=seed+index*1_000_000)
                for index,split in enumerate(split_order) if (count:=sizes.get(split)) is not None}
    assert_disjoint(partitions)
    return partitions
