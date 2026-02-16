# Physical observables and measurable proxies

Let κ(x,t) be coherence density, τ(x,t) responsibility, Σ(x,t) separation load.

## Field observables (directly computable)
1) Total coherence (mass):
M(t) = ∫ κ dx

2) Spatial coherence contrast:
C(t) = (max κ - min κ) / (mean κ + ε)

3) Separation burden (κ-weighted):
B(t) = (∫ Σ κ dx) / (∫ κ dx)

4) Temporal responsibility (κ-weighted):
T(t) = (∫ τ κ dx) / (∫ κ dx)

5) Pattern scale (structure factor peak):
S(k) = |FFT(κ - mean κ)|², define k* = argmax_{k≠0} S(k)

## Measurable mapping (examples)
- In cold atoms / optics: κ ↔ intensity or density; contrast C(t) ↔ visibility.
- Σ can be mapped to controlled dephasing/loss rate; B(t) predicts decay rate if Σ enters gain/loss in ψ-core.
- τ can be mapped to feedback/control parameter (e.g., phase locking strength, error-correction duty cycle).

## Falsifiable prediction (κ,Σ functional)
If a ψ-core with non-Hermitian damping γ(Σ) is used, predicted visibility obeys:
V(t) ≈ V(0) exp(-∫ Γ(t) dt)
Γ(t) = (∫ γ(Σ) κ dx)/(∫ κ dx)
