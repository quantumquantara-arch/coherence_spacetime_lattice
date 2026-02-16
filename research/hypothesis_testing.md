# Hypothesis Testing Framework

## Null Hypothesis H₀:
Temporal responsibility τ does not affect long-term coherence retention.

## Alternative H₁:
Higher τ statistically increases sustained κ over time.

Protocol:

1. Generate ensemble of simulations.
2. Randomize initial τ.
3. Measure slope of ⟨κ⟩ over time.
4. Perform regression:

⟨κ⟩_slope = β τ₀ + ε

Reject H₀ if p < 0.05.

---

## Geometry Hypothesis

H₀: Curvature proxy independent of κ gradients.  
H₁: |R_proxy| correlates with |∇²κ|.

Compute Pearson correlation across grid.

