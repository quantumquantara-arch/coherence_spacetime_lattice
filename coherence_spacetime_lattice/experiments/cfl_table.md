# CFL / stability experiments

For explicit Euler on u_t = D Δu in 2D with 5-point Laplacian:
dt ≤ dx² / (4D) is a standard sufficient bound.

Required experiment:
- choose D
- run explicit Euler at dt = c * dx²/D for c in {0.10,0.20,0.24,0.26,0.30}
- detect blow-up threshold (norm growth, NaNs)
- record c_max(dx) and show it approaches ~0.25 from below.

For IMEX (implicit diffusion), diffusion CFL is removed; remaining limitation comes from reactions:
dt ≤ 1 / max|∂F/∂u| (empirical) to avoid overshoot, plus invariance enforcement.
