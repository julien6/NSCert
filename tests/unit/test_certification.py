import math
import pytest
from invariant_mawm.certification import *

def test_budget_and_zero_bound():
    assert effective_budget(10)==3600
    assert zero_violation_bound(100,delta=.05,budget=1)==min(1,math.log(20)/100)

def test_cp_and_promote():
    assert .25 < clopper_pearson_upper(0,10,.05) < .27
    assert [promote(x) for x in [.5,.9,.99]]==["REJECTED","SOFT","HARD"]

def test_large_cp_is_finite_and_inputs_validated():
    bound=clopper_pearson_upper(2,40_000,.05)
    assert math.isfinite(bound) and 2/40_000 <= bound <= 1
    with pytest.raises(ValueError): zero_violation_bound(2,delta=1)
    with pytest.raises(ValueError): effective_budget(0)
