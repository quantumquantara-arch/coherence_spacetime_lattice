import numpy as np
from benchmarks.analytic_diffusion import gaussian_2d, variance, analytic_variance
from src.numerics.fd_imex import implicit_diffuse

def test_diffusion_variance_scaling():
    H=W=128
    D=0.2
    sigma0=1.5
    T=0.5
    for dx in [1.0, 0.5]:
        dt = 0.1*dx*dx/D
        steps = int(T/dt)
        u = gaussian_2d(H,W,dx,sigma0)
        v0 = variance(u,dx)
        for _ in range(steps):
            u = implicit_diffuse(u, D, dt, dx)
            u = np.maximum(u, 0.0)
            u /= np.sum(u)
        vT = variance(u,dx)
        target = v0 + analytic_variance(D, steps*dt)
        rel_err = abs(vT-target)/(abs(target)+1e-12)
        assert rel_err < 0.15
