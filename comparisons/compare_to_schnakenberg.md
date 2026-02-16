# Comparative simulations vs standard pattern-formation models

Goal: show what is genuinely different from classic Turing systems.

## Baselines
1) Schnakenberg (2-field):
u_t = Du Δu + a - u + u^2 v
v_t = Dv Δv + b - u^2 v

2) Gray–Scott:
u_t = Du Δu - uv^2 + F(1-u)
v_t = Dv Δv + uv^2 - (F+k)v

3) Your 3-field safe kinetics:
(κ,τ,Σ) system with φ(Σ)=1/(1+Σ)

## Comparison protocol
- Match domain, dx, dt, boundary conditions, and solver family.
- Match instability type: pick parameters so each model produces spots/stripes.
- Compare:
  a) structure factor peak k*
  b) coarsening rate
  c) amplitude statistics (histogram of κ)
  d) robustness under noise
  e) transient times to pattern onset

Deliverable: a single notebook/script that runs all models and exports identical metrics.
