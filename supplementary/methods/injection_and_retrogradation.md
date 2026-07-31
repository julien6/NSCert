# Rule lifecycle and injection

The lifecycle uses configured soft, hard, and stricter re-promotion thresholds. Hard
rules remove their affected feature from the neural target and supply a symbolic
prediction. Soft rules retain the neural target and contribute a configurable symbolic
consistency penalty. Other statuses use the neural target without a symbolic penalty.

Every relevant training transition increments the at-risk denominator. A counterexample
to a hard rule immediately changes its status to `RETROGRADED`, records dataset and
timestep provenance, and restores the neural target. Re-promotion rejects reused
evidence datasets, applies the stricter threshold, and is capped by `R_max`; exceeding
the cap marks the rule `NON_CERTIFIABLE`.
