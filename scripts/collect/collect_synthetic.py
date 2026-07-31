#!/usr/bin/env python3
"""Collect a small CounterWorld partition bundle as JSON Lines."""
import argparse, json
from dataclasses import asdict
from pathlib import Path
from invariant_mawm.collection import collect_partitions
from invariant_mawm.environments import CounterWorld, CounterWorldConfig

def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--episodes",type=int,default=2)
    parser.add_argument("--seed",type=int,default=0)
    args=parser.parse_args(); args.output.mkdir(parents=True,exist_ok=True)
    partitions=collect_partitions(lambda:CounterWorld(CounterWorldConfig()),
                                  {name:args.episodes for name in ("Dprop","Dfit","Dtest","Dshift")},seed=args.seed)
    for split,records in partitions.items():
        with (args.output/f"{split}.jsonl").open("w") as stream:
            for record in records: stream.write(json.dumps(asdict(record),sort_keys=True)+"\n")

if __name__=="__main__": main()
