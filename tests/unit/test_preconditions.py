import pytest
from invariant_mawm.core import Precondition
from invariant_mawm.preconditions import canonicalize, screen, validate

def test_commutative_canonicalization():
    a=Precondition("eq",("f0",1)); b=Precondition("eq",(1,"f0"))
    assert canonicalize(a)==canonicalize(b)

def test_depth_and_screening():
    p=Precondition("and",(Precondition("eq",("x",1)),Precondition("eq",("y",2))))
    validate(p,2)
    with pytest.raises(ValueError): validate(Precondition("and",(p,)),2)
    reasons=screen([1]*10,[False]*10,[0]*10,n_min=3)
    assert {"constant_reading","rare_precondition","insufficient_conditional_support"} <= set(reasons)

def test_screen_validates_and_handles_empty():
    assert "insufficient_conditional_support" in screen([],[],[])
    with pytest.raises(ValueError): screen([1],[True],[])
    result=screen([1],[True],[2],n_min=2,action_branches={"left":1},split="Dtest")
    assert "inadequate_action_branch_support" in result
    assert "prohibited_split_leakage" in result
