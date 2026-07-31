import json
import pytest
from invariant_mawm.core import Precondition, Reading, Transport
from invariant_mawm.proposers import EnumerativeProposer

def test_enumeration_is_deterministic_typed_and_accounted(tmp_path):
    readings=[Reading("scalar",("b",),{"value_type":"numeric"}),
              Reading("categorical",("a",),{"value_type":"categorical"})]
    transports=[Transport("affine",{"supported_types":["numeric"]})]
    proposer=EnumerativeProposer(readings,[Precondition("action",("go",))],transports,[1,0],seed=4)
    rules=list(proposer.propose())
    assert len(rules)==2
    assert proposer.statistics.predicted_count==4
    assert proposer.statistics.incompatible_count==2
    assert [r.invariant.memory_order for r in rules]==[0,1]

def test_resume_skips_completed_candidates(tmp_path):
    path=tmp_path/"resume.jsonl"
    args=([Reading("scalar",("x",))],[Precondition("action",("go",))],[Transport("affine")],[0])
    assert len(list(EnumerativeProposer(*args,resume_path=path).propose()))==1
    resumed=EnumerativeProposer(*args,resume_path=path)
    assert list(resumed.propose())==[] and resumed.statistics.resumed_count==1
    path.write_text("not-json\n")
    with pytest.raises(ValueError): list(EnumerativeProposer(*args,resume_path=path).propose())

