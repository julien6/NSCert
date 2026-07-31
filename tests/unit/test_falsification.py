import pytest
from invariant_mawm.falsification import GateEvidence, run_gate_ladder

def evidence(gate,dataset,violations=0,support=1000):
    return GateEvidence(gate,max(2000,support),support,violations,(dataset,))

def test_gate_ladder_passes_in_order_and_stops_on_failure():
    passed=run_gate_ladder([evidence("F1","holdout",support=10000)],maximum_violation_rate=.001)
    assert passed.stopped_after is None and passed.results[0].passed
    failed=run_gate_ladder([evidence("F1","holdout",20),evidence("F2","active")])
    assert failed.stopped_after=="F1" and len(failed.results)==1

def test_gate_ladder_rejects_order_and_dataset_reuse():
    with pytest.raises(ValueError): run_gate_ladder([evidence("F2","x")])
    with pytest.raises(ValueError): run_gate_ladder([evidence("F1","x",support=10000),evidence("F2","x")],maximum_violation_rate=.01)
