# Anytime-valid episode-level violation certificate

## Construction

Let `X_n` be the indicator that the retained relevant observation from episode `n`
violates a rule. The implementation conservatively uses the logical `any` of all
relevant transition violations in that episode. It therefore does not assume that
transitions inside an episode are independent.

For confidence level `delta`, allocate

\[
\delta_n = \frac{\delta}{n(n+1)}.
\]

At episode `n`, construct a one-sided Clopper--Pearson upper interval with error
probability `delta_n` from `X_1, ..., X_n`.

## Proposition

If episode-level indicators are IID Bernoulli with violation probability `p`, then with
probability at least `1-delta`, every reported upper endpoint contains `p`
simultaneously. Consequently, the endpoint remains valid at an arbitrary stopping time.

## Proof

For each fixed `n`, exact-binomial coverage gives failure probability at most
`delta_n`. The identity

\[
\sum_{n=1}^{\infty}\frac{1}{n(n+1)}=1
\]

and a union bound imply that the probability of at least one failure is at most
`sum(delta_n) = delta`. Simultaneous coverage immediately implies coverage at any
data-dependent stopping time. This construction handles within-episode dependence only
through conservative episode aggregation; it does not justify dependent episodes.

## Trade-off

Error spending is simple and auditable but generally wider than mixture-martingale
confidence sequences. It is provided as a defensible reconstruction pending access to
the paper's authoritative statistical reference.
