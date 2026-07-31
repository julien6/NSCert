import pytest
from invariant_mawm.core import PromotionStatus
from invariant_mawm.injection import ManagedRule,RuleLifecycle,injection_decision

def test_hard_rule_retrogrades_and_restores_neural_target():
    rule=ManagedRule("r"); lifecycle=RuleLifecycle()
    assert lifecycle.promote(rule,.999,{"F1"}) is PromotionStatus.HARD
    assert not injection_decision(rule,3).neural_target
    rule.observe(violated=True,dataset_id="training",timestep=8)
    assert rule.status is PromotionStatus.RETROGRADED
    assert injection_decision(rule,3).neural_target
    assert rule.retrogradation_history[0]["timestep"]==8

def test_repromotion_requires_fresh_data_and_is_capped():
    rule=ManagedRule("r"); lifecycle=RuleLifecycle(r_max=1)
    lifecycle.promote(rule,.999,{"old"}); rule.observe(violated=True,dataset_id="train",timestep=1)
    with pytest.raises(ValueError): lifecycle.promote(rule,.999,{"old"})
    assert lifecycle.promote(rule,.9,{"fresh"}) is PromotionStatus.PENDING_REPROMOTION
    assert lifecycle.promote(rule,1.0,{"newer"}) is PromotionStatus.NON_CERTIFIABLE

def test_soft_rule_keeps_neural_target_with_penalty():
    rule=ManagedRule("r",PromotionStatus.SOFT)
    decision=injection_decision(rule,2,soft_weight=.4)
    assert decision.neural_target and decision.soft_penalty_weight==.4
