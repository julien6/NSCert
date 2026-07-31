import random
from invariant_mawm.certification import AnytimeBernoulliCS

def test_anytime_sequence_updates_and_episode_subsamples():
    sequence=AnytimeBernoulliCS(.05)
    first=sequence.update_episode([False,False])
    second=sequence.update_episode([False,True,False])
    assert (first.support,first.violations)==(1,0)
    assert (second.support,second.violations)==(2,1)
    assert second.allocated_delta < first.allocated_delta

def test_anytime_simulation_has_conservative_small_sample_coverage():
    rng=random.Random(3); failures=0; probability=.2
    for _ in range(200):
        sequence=AnytimeBernoulliCS(.05); covered=True
        for _ in range(30):
            point=sequence.update(rng.random()<probability)
            covered &= point.upper_bound>=probability
        failures+=not covered
    assert failures<=10
