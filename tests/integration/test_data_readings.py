import pytest
from invariant_mawm.core import Reading
from invariant_mawm.data import Transition, assert_disjoint
from invariant_mawm.readings import anonymize, evaluate

def record(ds,ep,env="env",obs=1):
    return Transition(ds,env,"1","base","random","random",ep,0,0,{"x":obs},0,{"x":2})

def test_split_leakage_rejected():
    with pytest.raises(ValueError): assert_disjoint({"Dprop":[record("a","e")],"Dfit":[record("b","e")]})

def test_anonymization_deterministic_and_private():
    a=anonymize(["health","x"],7); b=anonymize(["health","x"],7)
    assert a.mapping_hash==b.mapping_hash
    assert not set(a.public.values()) & {"health","x"}
    assert evaluate(Reading("difference",("x","y")),{"x":4,"y":1})==3

def test_content_duplicate_and_environment_episode_identity():
    with pytest.raises(ValueError):
        assert_disjoint({"Dprop":[record("a","one")],"Dfit":[record("b","two")]})
    assert_disjoint({"Dprop":[record("a","same","env1",1)],
                     "Dfit":[record("b","same","env2",3)]})

def test_reversible_rescaling_and_slots():
    a=anonymize(["x"],3,True,["left","right"],{"x":(0,10)},True)
    transformed=a.transform({"x":5})
    assert a.reverse(transformed)=={"x":5}
    assert set(a.slot_public)=={"left","right"}
    with pytest.raises(ValueError): anonymize(["x","x"],0)
