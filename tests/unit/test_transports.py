import pytest
from invariant_mawm.transports import bounded_affine, delayed_copy, fit_affine, infer_permutation

def test_affine_and_clipping():
    assert bounded_affine(5,"up",alpha=1,offsets={"up":2},lower=0,upper=6)==6

def test_fit_persistence():
    got=fit_affine([1,2,3],[1,2,3],["a"]*3)
    assert got["alpha"]==1 and got["offsets"]["a"]==0

def test_delayed_and_permutation():
    assert delayed_copy([1,2,3],1)==2
    assert infer_permutation(["a","b"],["b","a"])==(1,0)
    with pytest.raises(IndexError): delayed_copy([1],2)

def test_fit_accepts_iterables_and_rejects_nonfinite():
    got=fit_affine(iter([0,1]),iter([1,2]),iter(["a","a"]))
    assert got["sample_count"]==2 and got["action_support"]=={"a":2}
    with pytest.raises(ValueError): fit_affine([float("nan")],[1],["a"])
