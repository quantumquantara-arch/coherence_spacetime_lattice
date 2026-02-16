# Unified κ–τ–Σ Field Equation (Working Research Note)

## 1. Variables and interpretation (dimensionless)

- **κ(x,t) ∈ [0,1]**: coherence density (order / phase-lock / resource proxy)
- **τ(x,t) ∈ [0,1]**: temporal responsibility (continuity / stability bias)
- **Σ(x,t) ∈ [0,∞)**: systemic separation (fragmentation / hidden entropy-like load)

This framework is an **explicit hypothesis**: stable spacetime-like behavior is treated as an emergent regime of high κ sustained by τ in the presence of Σ.

## 2. Unified reaction–diffusion PDE

Let x ∈ Ω ⊂ ℝ², t ≥ 0. Define

\[
\partial_t \kappa = D_\kappa \nabla^2 \kappa + F_\kappa(\kappa,\tau,\Sigma)
\]
\[
\partial_t \tau = D_\tau \nabla^2 \tau + F_\tau(\kappa,\tau,\Sigma)
\]
\[
\partial_t \Sigma = D_\Sigma \nabla^2 \Sigma + F_\Sigma(\kappa,\tau,\Sigma)
\]

with diffusion coefficients \(D_\kappa,D_\tau,D_\Sigma \ge 0\).

### 2.1 A concrete closed form used in code

The reference implementation uses:

\[
F_\kappa = a_\kappa\, \tau^{p}\,\kappa(1-\kappa) - \lambda_\kappa \Sigma^{q}\kappa
\]

\[
F_\tau = a_\tau\,\kappa(1-\tilde{\Sigma})(1-\tau) - \lambda_\tau \Sigma^{q}\tau,\quad \tilde{\Sigma}=\min(\Sigma,1)
\]

\[
F_\Sigma = a_\Sigma(1-\tau)\kappa - \lambda_\Sigma \Sigma
\]

Parameters \(a_\*\), \(\lambda_\*\) are nonnegative; exponents \(p,q\) tune gating and penalty nonlinearity.

This is not claimed as fundamental physics; it is a minimal mathematically-defined dynamical system that supports:
- coherent pulse propagation and spreading (via diffusion),
- stabilization via τ-feedback,
- degradation via Σ-load.

## 3. Discretization on a 2D lattice

Let the grid be \(y=0..H-1\), \(x=0..W-1\) with spacing \(\Delta x\). The 5-point Laplacian:

\[
\nabla^2 u_{y,x} \approx \frac{u_{y+1,x}+u_{y-1,x}+u_{y,x+1}+u_{y,x-1}-4u_{y,x}}{(\Delta x)^2}
\]

Time stepping (explicit Euler):

\[
u^{n+1} = u^n + \Delta t \left(D\nabla^2 u^n + F(u^n)\right)
\]

### 3.1 Stability (explicit diffusion)

For the 2D 5-point Laplacian, a conservative bound is:

\[
\Delta t \le \frac{(\Delta x)^2}{4 D_{\max}}
\]

where \(D_{\max}=\max(D_\kappa,D_\tau,D_\Sigma)\).

## 4. Emergent geometry proxy (toy)

Define a coherence potential:

\[
\Phi = \kappa - \langle \kappa \rangle
\]

Define a conformal scale factor:

\[
\Omega = 1 + \alpha \Phi,\quad \Omega>0
\]

Define a curvature proxy (2D conformal form):

\[
R_{\text{proxy}} = - \nabla^2 \log(\Omega)
\]

These quantities are computed deterministically from the field and are used for empirical exploration.

## 5. Validation targets (what can be tested)

- Boundedness: κ,τ remain in [0,1]; Σ remains ≥ 0 (enforced in code).
- Numerical stability: explicit dt is checked against diffusion bound.
- Regression invariants:
  - deterministic stepping under fixed seed/noise=0
  - monotone tendencies in toy “free-energy-like” functional under small dt (qualitative)

## 6. What “inversion” means operationally (repo-level)

Standard approaches start with spacetime + quantum states-on-spacetime.
This repo’s operational inversion is:
- dynamics are written in κ–τ–Σ first,
- geometry proxies are *computed from κ* afterward,
- comparisons are made between histories (“temporal channels”) via τ-weighted coherence retention.

That is a computational claim (the code runs), not a settled physical claim.
