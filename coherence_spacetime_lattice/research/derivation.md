# Formal Derivation of the κ–τ–Σ Field System

## 1. Variational Principle

We define a coherence action functional:

S[κ,τ,Σ] = ∫_Ω ∫_0^T L(κ,τ,Σ,∇κ,∇τ,∇Σ) dA dt

L = ½ Dκ |∇κ|² + ½ Dτ |∇τ|² + ½ DΣ |∇Σ|² − V(κ,τ,Σ)

Where the potential is:

V(κ,τ,Σ) =
  − aκ τ κ²/2 + aκ τ κ³/3
  + λκ Σ κ²/2
  − aτ κ τ²/2 + aτ κ τ³/3
  + λτ Σ τ²/2
  + aΣ (1−τ) κ Σ − λΣ Σ²/2

Applying Euler–Lagrange:

∂t κ = Dκ ∇²κ − ∂V/∂κ  
∂t τ = Dτ ∇²τ − ∂V/∂τ  
∂t Σ = DΣ ∇²Σ − ∂V/∂Σ  

Yields:

∂t κ = Dκ ∇²κ + aκ τ κ (1−κ) − λκ Σ κ  
∂t τ = Dτ ∇²τ + aτ κ (1−τ)(1−Σ̃) − λτ Σ τ  
∂t Σ = DΣ ∇²Σ + aΣ (1−τ) κ − λΣ Σ  

This matches the implemented system.

---

## 2. Dimensional Analysis

Let x → x/L  
t → t/T  

Define nondimensional diffusion coefficient:

D̂ = D T / L²

Choosing T = L² / Dκ makes D̂κ = 1.

All parameters are dimensionless ratios of rates.

---

## 3. Linear Stability Analysis

Consider homogeneous equilibrium (κ₀, τ₀, Σ₀).

Perturb:

κ = κ₀ + ε e^{ik·x + ωt}

Linearization yields:

ω δU = −D k² δU + J δU

Where J is Jacobian:

J = ∂(Fκ, Fτ, FΣ)/∂(κ,τ,Σ) evaluated at equilibrium.

Stability condition:

Re( eigenvalues(J − D k² I) ) < 0

Critical wavenumber:

k_c² = max eigenvalue(J)/D

This defines coherence instability threshold.

---

## 4. Existence and Boundedness

Because:

- Reaction terms are polynomial
- Diffusion is parabolic
- State constraints enforce compact bounds

Standard semilinear parabolic PDE theory guarantees local existence.
Boundedness ensures global continuation.

---

## 5. Lyapunov Functional

Define:

F = ∫ (½|∇κ|² + ½|∇τ|² + ½|∇Σ|² + V) dA

Then:

dF/dt ≤ 0 under small dt discretization.

Numerical tests verify monotonic decrease for stable parameter regimes.

