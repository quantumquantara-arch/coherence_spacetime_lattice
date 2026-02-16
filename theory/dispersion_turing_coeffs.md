# Full Dispersion Relation and Bifurcation Analysis

**Cubic dispersion polynomial** (derived explicitly):
\[
\chi(\lambda;\mu) = \lambda^3 + a_1(\mu)\lambda^2 + a_2(\mu)\lambda + a_3(\mu) = 0
\]
with $a_1,a_2,a_3$ as polynomials in $\mu=k^2$ (exact coefficients in SymPy notebook).

**Turing conditions** (necessary + sufficient): homogeneous stable ($a_1(0)>0$, $a_3(0)>0$, $a_1a_2>a_3$ at $\mu=0$) but $\max\operatorname{Re}\lambda(\mu)>0$ for some $\mu>0$ (verified by Sturm sequence or numerical root tracking).

**Codimension-2 points**: Turing-Hopf loci solved by simultaneous $a_1(\mu)=0$, $\operatorname{Im}\lambda=0$ (explicit in nonlinear_continuation.py).

**Pseudo-arclength continuation** implemented and verified in research/scripts/nonlinear_continuation.py.
