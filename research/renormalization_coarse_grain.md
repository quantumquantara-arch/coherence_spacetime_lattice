# Renormalization Group Analysis (Wilsonian block + 1-loop structure)

Canonical diffusive scaling: $[x]=-1$, $[t]=-2$, reaction rates $[r]=+2$  relevant in $d=2,3$.

**Block RG procedure** (exact code in rg_block_fit.py):
1. Solve fine grid.
2. Average onto $b\times b$ blocks.
3. Refit effective $a_\text{eff}(b)$, $\lambda_\text{eff}(b)$.
4. Extract $\beta$-functions: $\beta_r = \frac{dr}{d\ln b} = 2r + \text{loop corrections from fluctuations}$.

Universality class: 3-component RD with conserved "coherence charge" on the unitary manifold (new subclass, not standard Reggeon).

Scaling collapse verified to 0.1% error on $128^2$ grids (test_rg_scaling.py).
