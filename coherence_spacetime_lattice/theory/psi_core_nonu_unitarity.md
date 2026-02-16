# ψ-Core With Non-Hermitian Coupling: Coherence–Decoherence Modulators (τ, Σ)

## 0. Scope and aim

This document replaces the inconsistent “κ reaction cancellation” story with a consistent coupled-field theory in which:

- **ψ(x,t) ∈ ℂ** is the primary (quantum-like) complex amplitude field.
- **κ(x,t) := |ψ(x,t)|²** is the coherence density (probability density / intensity).
- **τ(x,t) ∈ [0,1]** is a responsibility/locking field that promotes coherence retention.
- **Σ(x,t) ≥ 0** is a separation load field that promotes decoherence/damping.

The core principle is:

- ψ is **unitary** when the coupling is **Hermitian** (no gain/loss term).
- Apparent non-unitarity arises from a **controlled non-Hermitian** (imaginary potential) coupling that is **itself dynamical** via (τ, Σ).
- “Emergent unitarity” means the system dynamically approaches a manifold where the gain/loss term vanishes (pointwise or κ-weighted).

No κ-equation with independent reaction terms is postulated; κ evolves from ψ.

---

## 1. Explicit ψ equation with non-Hermitian coupling

Let Ω ⊂ ℝᵈ be a bounded smooth domain (or periodic torus). Consider:

\[
i\,\partial_t \psi
=
- D \nabla^2 \psi
+ V(\kappa,\tau,\Sigma)\,\psi
+ i\,G(\kappa,\tau,\Sigma)\,\psi,
\qquad
\kappa = |\psi|^2,
\]

where:

- D>0 is a dispersion/diffusion parameter (set by scaling; D = ħ/(2m) in Schrödinger units).
- V is a **real-valued** potential functional (Hermitian part).
- G is a **real-valued** gain/loss functional (non-Hermitian part).

A minimal and testable choice:

\[
G(\kappa,\tau,\Sigma) = \eta\,\tau\, (1-\kappa) - \gamma(\Sigma),
\qquad
\gamma(\Sigma)=\gamma_0+\gamma_1 \Sigma,
\]

with parameters η, γ0, γ1 ≥ 0. Interpretation:

- η τ (1−κ) is a bounded *coherence replenishment* term driving κ toward 1 where τ is high.
- γ(Σ) is a *decoherence/damping* term increasing with Σ.

**Unitary core limit:** set G ≡ 0 (e.g., η=0 and γ0=γ1=0, or τ=0 and Σ=0), then ψ evolves unitarily under the Hermitian operator −D∇²+V.

---

## 2. Correct mass-balance identity (exact)

Define κ=|ψ|². Multiply the ψ equation by ψ* and subtract its complex conjugate.

The local continuity equation is:

\[
\partial_t \kappa + \nabla \cdot j = 2\,G(\kappa,\tau,\Sigma)\,\kappa,
\]

with current

\[
j = 2D\,\mathrm{Im}(\psi^* \nabla \psi).
\]

Integrate over Ω with periodic BC or Neumann BC (so ∫∂Ω j·n = 0):

\[
\frac{d}{dt}\int_\Omega \kappa\,dx
=
2\int_\Omega G(\kappa,\tau,\Sigma)\,\kappa\,dx.
\]

Therefore:

- If G ≡ 0 pointwise, **mass is conserved exactly** (unitarity).
- If G is nonzero, the deviation from unitarity is quantified exactly by the κ-weighted integral of G.

This is the correct replacement for any “κ reaction cancellation” story.

---

## 3. Invariant-region-safe τ, Σ kinetics (forward invariance)

We require τ(x,t) ∈ [0,1] and Σ(x,t) ≥ 0 to be **forward invariant** under the PDE dynamics.

Use diffusion plus reaction terms chosen to be inward-pointing on the boundaries:

\[
\partial_t \tau
=
D_\tau \nabla^2 \tau
+ a_\tau\,\kappa\,(1-\tau)\,\phi(\Sigma)
- \lambda_\tau\,\Sigma\,\tau,
\]

\[
\partial_t \Sigma
=
D_\Sigma \nabla^2 \Sigma
+ a_\Sigma\,(1-\tau)\,\kappa
- \lambda_\Sigma\,\Sigma,
\]

with parameters Dτ,DΣ,aτ,aΣ,λτ,λΣ > 0 and any **bounded, nonnegative** modulation function φ(Σ) satisfying:

- φ(Σ) ∈ [0,1] for all Σ ≥ 0,
- φ is smooth and nonincreasing (typical).

Two standard choices:

- \(\phi(\Sigma)=\frac{1}{1+\Sigma}\)
- \(\phi(\Sigma)=e^{-\Sigma}\)

### 3.1 Proof sketch of forward invariance (maximum principle arguments)

Assume κ ≥ 0 (true by definition κ=|ψ|²).

**(i) Σ ≥ 0:**  
At Σ=0, reaction term is \(a_\Sigma(1-\tau)\kappa \ge 0\). Diffusion cannot create negative minima under Neumann/periodic BC by the maximum principle. Hence Σ(t) stays ≥ 0.

**(ii) τ ≥ 0:**  
At τ=0, reaction term is \(a_\tau \kappa(1-0)\phi(\Sigma) \ge 0\) and the sink term −λτ Σ τ vanishes. Hence τ cannot cross below 0.

**(iii) τ ≤ 1:**  
At τ=1, the source term \(a_\tau \kappa(1-\tau)\phi(\Sigma)\) vanishes and the sink term is −λτ Σ ≤ 0, so τ is pushed inward.

Therefore τ ∈ [0,1] and Σ ≥ 0 are forward invariant (in the classical PDE sense) provided the discretization respects the maximum principle (e.g., monotone schemes / sufficiently small dt in explicit methods).

This fixes the earlier structural flaw from factors like (1−Σ) that can go negative when Σ>1.

---

## 4. Explicit slaving (adiabatic elimination) in the fast-(τ,Σ) limit (κ-dependent)

Assume τ and Σ relax much faster than ψ/κ, e.g.:

- λτ, λΣ are large (fast reaction),
- or Dτ,DΣ are large compared to ψ timescales,
- or κ varies slowly in time compared to τ,Σ.

Then at leading order, set τ_t ≈ 0 and Σ_t ≈ 0 **locally** (dropping diffusion first):

### 4.1 Σ quasi-steady state

\[
0 = a_\Sigma(1-\tau)\kappa - \lambda_\Sigma \Sigma
\quad\Rightarrow\quad
\Sigma = \Sigma^*(\kappa,\tau) = \frac{a_\Sigma}{\lambda_\Sigma}(1-\tau)\kappa.
\]

### 4.2 τ quasi-steady state (implicit)

\[
0 = a_\tau \kappa(1-\tau)\phi(\Sigma) - \lambda_\tau \Sigma \tau.
\]

Substitute Σ = Σ*(κ,τ):

\[
a_\tau \kappa(1-\tau)\,\phi\!\left(\frac{a_\Sigma}{\lambda_\Sigma}(1-\tau)\kappa\right)
=
\lambda_\tau \left(\frac{a_\Sigma}{\lambda_\Sigma}(1-\tau)\kappa\right)\tau.
\]

If κ>0 and (1−τ)≠0, cancel κ(1−τ):

\[
a_\tau\,
\phi\!\left(\frac{a_\Sigma}{\lambda_\Sigma}(1-\tau)\kappa\right)
=
\frac{\lambda_\tau a_\Sigma}{\lambda_\Sigma}\,\tau.
\]

Define the constant:

\[
C := \frac{\lambda_\tau a_\Sigma}{\lambda_\Sigma}.
\]

Then τ must satisfy the **κ-dependent implicit equation**:

\[
\tau = \frac{a_\tau}{C}\,
\phi\!\left(\frac{a_\Sigma}{\lambda_\Sigma}(1-\tau)\kappa\right).
\]

This shows explicitly:

- τ* is generally **not constant**; it depends on κ through the argument of φ.
- For φ decreasing, τ decreases as κ increases (more κ drives Σ, which suppresses τ production).

### 4.3 Emergent unitarity manifold (slaved form)

Recall the exact mass balance:

\[
\frac{d}{dt}\int \kappa\,dx = 2\int (\eta \tau (1-\kappa)-\gamma(\Sigma))\,\kappa\,dx.
\]

A strong “unitarity manifold” is the **pointwise** condition:

\[
\eta \tau(1-\kappa) = \gamma(\Sigma).
\]

Under slaving, Σ = Σ*(κ,τ), so:

\[
\eta \tau(1-\kappa)
=
\gamma\!\left(\frac{a_\Sigma}{\lambda_\Sigma}(1-\tau)\kappa\right).
\]

This is an explicit κ-dependent manifold in (κ,τ) (and thus in κ alone if τ is further reduced by the implicit relation above).

A weaker, experimentally aligned “effective unitarity” condition is κ-weighted:

\[
\int (\eta \tau (1-\kappa)-\gamma(\Sigma))\,\kappa\,dx \approx 0.
\]

---

## 5. Falsifiable prediction as a functional of Σ and κ (no handwaving)

Define the **κ-weighted decoherence rate functional**:

\[
\Gamma(t)
:=
\frac{\int_\Omega \gamma(\Sigma(x,t))\,\kappa(x,t)\,dx}{\int_\Omega \kappa(x,t)\,dx}.
\]

For \(\gamma(\Sigma)=\gamma_0+\gamma_1\Sigma\):

\[
\Gamma(t) = \gamma_0 + \gamma_1\,\frac{\int \Sigma\,\kappa\,dx}{\int \kappa\,dx}.
\]

### Prediction P1 (visibility decay law)
In a two-path interference simulation (or experiment proxy) define visibility 𝒱(t) from the contrast of κ on a screen/region.
The model-level prediction is:

\[
\mathcal{V}(t)
\approx
\mathcal{V}(0)\,\exp\!\left(-\int_0^t \Gamma(t')\,dt'\right),
\]

provided:
- the primary decoherence enters through γ(Σ) in the gain/loss term,
- τ-driven pumping is either off (η=0) or separately accounted for by replacing γ with (γ−ητ(1−κ)) in Γ.

More generally, from the exact κ balance, define

\[
\Gamma_{\mathrm{net}}(t)
:=
\frac{\int_\Omega (\gamma(\Sigma)-\eta\tau(1-\kappa))\,\kappa\,dx}{\int_\Omega \kappa\,dx}.
\]

Then:

\[
\mathcal{V}(t)\approx \mathcal{V}(0)\exp\!\left(-\int_0^t \Gamma_{\mathrm{net}}(t')\,dt'\right).
\]

### Falsification criteria (internal-to-model and experimental proxy)
The prediction fails if any of the following holds:

1. Measured \(\log(\mathcal{V}(t)/\mathcal{V}(0))\) is not well-approximated by \(-\int_0^t \Gamma_{\mathrm{net}}(t')dt'\).
2. Changing initial κ while holding Σ fixed changes the decay in a way inconsistent with κ-weighting (i.e., violates the functional dependence above).
3. If Σ is externally forced and γ(Σ) is known, the visibility decay does not track the predicted integral functional.

This is a falsifiable statement because Γ_net is computed directly from the simulated/measured Σ,κ fields with no additional fit beyond γ(·).

---

## 6. Summary of what is fixed vs the old story

Replaced:
- “κ reaction cancellation” (inconsistent when κ=|ψ|²)

With:
- explicit ψ equation with a non-Hermitian gain/loss term iGψ
- exact mass-balance identity for κ derived from ψ
- τ,Σ kinetics guaranteeing τ∈[0,1], Σ≥0 via φ(Σ)≥0
- correct κ-dependent slaving relations τ*(κ), Σ*(κ,τ)
- falsifiable prediction stated as an explicit κ-weighted functional of Σ (and τ if included)

