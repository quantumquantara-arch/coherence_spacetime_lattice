from __future__ import annotations
import numpy as np

def laplacian_5pt(u: np.ndarray, dx: float) -> np.ndarray:
    up = np.pad(u, ((1,1),(1,1)), mode="edge")
    c = up[1:-1, 1:-1]
    n = up[:-2, 1:-1]
    s = up[2:,  1:-1]
    w = up[1:-1, :-2]
    e = up[1:-1, 2:]
    return (n+s+w+e-4.0*c)/(dx*dx)

def thomas_solve_tridiag(a,b,c,d):
    # a lower, b diag, c upper, d rhs
    n = len(b)
    cp = np.zeros(n-1)
    dp = np.zeros(n)
    cp[0] = c[0]/b[0]
    dp[0] = d[0]/b[0]
    for i in range(1,n-1):
        denom = b[i]-a[i-1]*cp[i-1]
        cp[i] = c[i]/denom
        dp[i] = (d[i]-a[i-1]*dp[i-1])/denom
    dp[n-1] = (d[n-1]-a[n-2]*dp[n-2])/(b[n-1]-a[n-2]*cp[n-2])
    x = np.zeros(n)
    x[n-1] = dp[n-1]
    for i in range(n-2,-1,-1):
        x[i] = dp[i]-cp[i]*x[i+1]
    return x

def implicit_diffuse(u: np.ndarray, D: float, dt: float, dx: float) -> np.ndarray:
    """
    ADI-style 2D diffusion step: (I - dt D Δ) u^{n+1} = u^n
    Two passes: x-implicit then y-implicit (Peaceman-Rachford).
    Neumann-like via edge padding in laplacian is not used here; instead solve with simple
    second-difference and reflective boundary by copying neighbor at edges.
    """
    r = D*dt/(dx*dx)
    v = u.copy()

    # x-implicit
    H,W = v.shape
    out = np.zeros_like(v)
    a = -r*np.ones(W-1)
    b = (1+2*r)*np.ones(W)
    c = -r*np.ones(W-1)
    for i in range(H):
        rhs = v[i,:].copy()
        # reflective BC adjustment (approx Neumann)
        rhs[0] += r*rhs[1]
        rhs[-1] += r*rhs[-2]
        bb = b.copy()
        bb[0] = 1+r
        bb[-1] = 1+r
        out[i,:] = thomas_solve_tridiag(a, bb, c, rhs)

    # y-implicit
    v2 = out
    out2 = np.zeros_like(v2)
    a = -r*np.ones(H-1)
    b = (1+2*r)*np.ones(H)
    c = -r*np.ones(H-1)
    for j in range(W):
        rhs = v2[:,j].copy()
        rhs[0] += r*rhs[1]
        rhs[-1] += r*rhs[-2]
        bb = b.copy()
        bb[0] = 1+r
        bb[-1] = 1+r
        out2[:,j] = thomas_solve_tridiag(a, bb, c, rhs)
    return out2

def step_imex(kappa, tau, sigma, params, dt, dx):
    """
    IMEX: implicit diffusion, explicit reactions.
    Enforces invariant region via safe kinetics + clipping as a numerical guardrail.
    """
    # implicit diffusion
    k = implicit_diffuse(kappa, params["Dk"], dt, dx)
    t = implicit_diffuse(tau,   params["Dt"], dt, dx)
    s = implicit_diffuse(sigma, params["Ds"], dt, dx)

    phi = 1.0/(1.0+s)  # safe choice

    # reactions
    fk = params["ak"]*t*k*(1-k) - params["lk"]*s*k
    gt = params["at"]*k*(1-t)*phi - params["lt"]*s*t
    hs = params["aS"]*(1-t)*k - params["lS"]*s

    k = k + dt*fk
    t = t + dt*gt
    s = s + dt*hs

    # enforce invariant region
    k = np.clip(k, 0.0, 1.0)
    t = np.clip(t, 0.0, 1.0)
    s = np.maximum(s, 0.0)
    return k,t,s
