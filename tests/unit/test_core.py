import json
import pytest
from invariant_mawm.core import Reading, Precondition, Transport, PartialInvariant, RuleInventory

def test_rule_id_is_deterministic():
    rule=PartialInvariant(Reading("scalar",("f0",)),Precondition("action",("left",)),Transport("affine",{"alpha":1}))
    assert rule.rule_id==rule.rule_id and len(rule.rule_id)==16

def test_inventory_rejects_incomplete_rule():
    with pytest.raises(ValueError): RuleInventory().add({"rule_id":"x"})

def test_inventory_validates_semantics():
    row={"rule_id":"x","reading":{},"precondition":{},"transport":{},"memory_order":0,
         "source_proposer":"P1","proposal_seed":0,"fit_dataset_id":"fit",
         "gate_results":{g:{} for g in ("F1","F2","F3","F4")},
         "empirical_violation_rate":0,"confidence_or_validity_score":1,
         "certificate_upper_bound":.1,"conditional_support":3,"trigger_frequency":.2,
         "feature_coverage":.2,"transition_coverage":.2,"promotion_status":"HARD",
         "retrogradation_history":[],"reproduction_metadata":{}}
    inv=RuleInventory(); inv.add(row); assert len(inv.rules)==1
    row["promotion_status"]="UNKNOWN"
    with pytest.raises(ValueError): RuleInventory().add(row)
