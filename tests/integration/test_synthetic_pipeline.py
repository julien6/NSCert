from invariant_mawm.collection import collect_partitions
from invariant_mawm.environments import CounterWorld, CounterWorldConfig
from invariant_mawm.evaluation import evaluate_affine
from invariant_mawm.falsification import GateEvidence, run_gate_ladder

def test_synthetic_collection_and_oracle_motion_certificate():
    config=CounterWorldConfig(agents=2,horizon=12)
    splits=collect_partitions(lambda:CounterWorld(config),{"Dprop":2,"Dfit":2,"Dtest":40,"Dshift":40},seed=9)
    assert all(len(records)==config.horizon*count for records,count in zip(splits.values(),(2,2,40,40)))
    evaluations=[]
    for split in ("Dtest","Dshift"):
        result=evaluate_affine(splits[split],feature="agent0.position",agent=0,alpha=1,
            offsets={-1:-1,0:0,1:1},lower=0,upper=7)
        assert result.violations==0
        evaluations.append(GateEvidence("F1" if split=="Dtest" else "F2",result.total_transitions,
            result.conditional_support,result.violations,(split,)))
    ladder=run_gate_ladder(evaluations,maximum_violation_rate=.02)
    assert ladder.stopped_after is None

def test_counterworld_is_seeded_and_validates_actions():
    first=CounterWorld(); second=CounterWorld()
    assert first.reset(4)==second.reset(4)
