# Closed-form Turing (diffusion-driven) instability inequalities for κ–τ–Σ

Let the homogeneous ODE be U̇ = F(U), U=(κ,τ,Σ). At a homogeneous equilibrium U*,
define the Jacobian J = DF(U*). For the PDE linearization around U*:

δU_t = (J - μ D) δU,     μ := k^2 ≥ 0,     D = diag(Dκ, Dτ, DΣ), Dκ,Dτ,DΣ>0.

The characteristic polynomial for A(μ) := J - μD is cubic:

χ(λ;μ) = det(λ I - A(μ)) = λ^3 + a1(μ) λ^2 + a2(μ) λ + a3(μ).

For a real 3×3 matrix, a sufficient and necessary condition for asymptotic stability
(all eigenvalues have negative real part) is the Routh–Hurwitz set:

( RH1 ) a1(μ) > 0
( RH2 ) a2(μ) > 0
( RH3 ) a3(μ) > 0
( RH4 ) a1(μ) a2(μ) > a3(μ)

Definitions in terms of invariants of A(μ):

a1(μ) = -tr(A(μ))
a2(μ) = sum of principal 2×2 minors of A(μ)
a3(μ) = -det(A(μ))

Because A(μ)=J-μD and D is diagonal, these become explicit low-degree polynomials in μ.

## 1. Explicit polynomials in μ

Write:
T0 := tr(J) = J11+J22+J33
S0 := sum principal minors of J
Δ0 := det(J)

Also:
TrD := tr(D)=Dκ+Dτ+DΣ
S_DJ := Dκ(J22+J33) + Dτ(J11+J33) + DΣ(J11+J22)          (weighted trace of J minors)
S_DD := DκDτ + DκDΣ + DτDΣ
ΔD := det(D) = Dκ Dτ DΣ

Then:

a1(μ) = -(T0 - μ TrD) = -T0 + μ TrD                         (linear)

a2(μ) = S0 - μ S_DJ + μ^2 S_DD                              (quadratic)

a3(μ) = -det(J - μD) = -(Δ0 - μ C1 + μ^2 C2 - μ^3 ΔD)       (cubic)

where the coefficients C1, C2 are closed-form:

C1 = Dκ M11 + Dτ M22 + DΣ M33
C2 = DκDτ J33 + DκDΣ J22 + DτDΣ J11

and Mii are principal cofactors of J:
M11 = det([[J22,J23],[J32,J33]])
M22 = det([[J11,J13],[J31,J33]])
M33 = det([[J11,J12],[J21,J22]])

So:

a3(μ) = -Δ0 + μ C1 - μ^2 C2 + μ^3 ΔD                        (cubic)

Finally define:
H(μ) := a1(μ) a2(μ) - a3(μ)                                  (cubic)

All coefficients are explicit in J and D.

## 2. Turing instability conditions (3-field)

A diffusion-driven instability exists if:

(T0) homogeneous stability: RH1–RH4 hold at μ=0:
  a1(0)>0, a2(0)>0, a3(0)>0, a1(0)a2(0)>a3(0)

(T1) there exists μ>0 such that at least one RH condition fails:
  a1(μ) ≤ 0  OR  a2(μ) ≤ 0  OR  a3(μ) ≤ 0  OR  H(μ) ≤ 0

Because a1,a2,a3,H are polynomials in μ, this reduces to checking whether any of
these polynomials crosses zero for μ>0. Closed-form roots (quadratic/cubic) exist
via standard formulas; in practice evaluate discriminants and real positive roots.

Common sharp trigger in 3-field systems is a3(μ)=0 (determinant crossing) or H(μ)=0
(complex pair crossing), but the full set above is exact.

## 3. Two-field reduction (closed inequalities)

If Σ is slaved/fast and reduced out, yielding a 2×2 Jacobian J2 and D2,
the classical closed-form Turing conditions apply:

Let tr2 = tr(J2), det2 = det(J2),
and Dκ,Dτ > 0. Homogeneous stability:
  tr2 < 0, det2 > 0.

Turing existence iff:
  (i) Dκ J2_22 + Dτ J2_11 > 2 sqrt(Dκ Dτ det2)
  (ii) det2 > 0, tr2 < 0
and additionally the discriminant of the μ-quadratic for det(J2-μD2)=0 is positive.

## 4. Implementation note

Use:
- compute J at equilibrium U*
- form coefficients above
- solve for positive real roots of a2(μ), a3(μ), H(μ), and check sign changes.
