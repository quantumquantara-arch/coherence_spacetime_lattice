# Renormalization-style coarse-graining for κ–τ–Σ reaction–diffusion

This is a controlled scaling analysis for the continuum PDE as a dynamical field theory.
It is not a claim of microscopic derivation; it gives testable scaling predictions.

## 1. Canonical (engineering) dimensions

PDE:
∂t U = D ∇² U + F(U),  U=(κ,τ,Σ)

Rescale:
x = b x',   t = b^z t',   choose z=2 (diffusive scaling)

Then:
∂t = b^{-z} ∂t' = b^{-2} ∂t'
∇² = b^{-2} ∇'²

So diffusion term is invariant if D is held fixed (D' = D).
Reaction term transforms as:
F'(U) = b^{-2} F(U)

Thus every reaction rate r in F has canonical scaling dimension:
r' = b^{2} r        (relevant under coarse-graining in d=2).

This predicts that at larger scales (coarser lattices) effective reaction rates grow
relative to diffusion unless compensated by parameter renormalization.

## 2. Practical coarse-graining experiment

Given a fine simulation with spacing Δx:

1) Evolve PDE for N steps at (Δx,Δt) with stable Δt ~ O(Δx²).
2) Block-average fields by factor b (e.g., 2×2 -> 1 cell):
   U_b(i,j) = mean over block.
3) Compare the blocked evolution to a coarse simulation run directly at spacing bΔx.
4) Fit effective parameters p_eff(b) minimizing:
   || U_b(t) - U_coarse(t; p_eff) ||_2 over multiple times.

This defines empirical RG flow p -> p_eff(b).

## 3. Observable scaling predictions

Define correlation length of κ:
ξ^2 = ∫ |x|^2 C(x) dx / ∫ C(x) dx,  C(x)=⟨(κ-⟨κ⟩)(κ(x+·)-⟨κ⟩)⟩

Near a pattern-forming instability (Turing boundary), expect:
ξ ~ (distance to critical)^{-ν}

Estimate ν from parameter scans; compare across block factors b to test scaling collapse.

## 4. Dynamic RG (loop corrections)

For stochastic extension:
∂t U = D∇²U + F(U) + η(x,t),  ⟨ηη⟩ ~ Γ δ(x-x')δ(t-t')

One can derive 1-loop corrections to reaction rates; the canonical statement remains:
in d=2, reactions are relevant under diffusive scaling.
The repo-level deliverable is the empirical p_eff(b) flow from block-fitting.

