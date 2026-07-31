# Assumptions and ambiguities

1. The confidence/validity score `q` is not defined in the supplied material. Promotion
   accepts a caller-provided probability and does not pretend it is a certificate.
2. Affine fitting restricts alpha to `{0,1}`, searches observed and mean per-action
   residuals against clipped squared error, and uses deterministic lower-alpha tie
   breaking. Bounds are observed target extrema; bounds outside observed saturation
   remain unidentifiable.
3. Exact slot assignment is factorial and intended only for small multi-agent smoke data.
4. The zero-violation expression is implemented exactly as the stated logarithmic upper
   bound (clipped to one); it is not substituted with a different exact-binomial result.
5. No scientific output is claimed until the paper and environment specifications exist.
