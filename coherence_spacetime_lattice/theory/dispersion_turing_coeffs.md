# Exact dispersion relation coefficients for 3-field RD with diagonal diffusion

Let A(μ) = J − μ D, with μ = |k|² ≥ 0 and D = diag(Dκ, Dτ, DΣ).

Characteristic polynomial:
χ(λ;μ) = det(λI − A(μ)) = λ³ + a1(μ) λ² + a2(μ) λ + a3(μ).

Invariants:
a1(μ) = −tr(A(μ))
a2(μ) = sum of principal 2×2 minors of A(μ)
a3(μ) = −det(A(μ))

Let:
T0 = tr(J)
S0 = sum principal 2×2 minors of J
Δ0 = det(J)
TrD = Dκ + Dτ + DΣ
SDD = DκDτ + DκDΣ + DτDΣ
detD = DκDτDΣ

Weighted minor-trace term:
SDJ = Dκ(J22+J33) + Dτ(J11+J33) + DΣ(J11+J22)

Diagonal cofactors of J:
M11 = det([[J22,J23],[J32,J33]])
M22 = det([[J11,J13],[J31,J33]])
M33 = det([[J11,J12],[J21,J22]])

C1 = Dκ M11 + Dτ M22 + DΣ M33
C2 = DκDτ J33 + DκDΣ J22 + DτDΣ J11

Then:
a1(μ) = −T0 + μ TrD
a2(μ) = S0 − μ SDJ + μ² SDD
a3(μ) = −Δ0 + μ C1 − μ² C2 + μ³ detD

Hurwitz determinant:
H(μ) := a1(μ)a2(μ) − a3(μ)

Exact Turing condition:
- stable at μ=0 (a1(0),a2(0),a3(0),H(0) > 0)
- exists μ>0 such that any of a1(μ),a2(μ),a3(μ),H(μ) ≤ 0
