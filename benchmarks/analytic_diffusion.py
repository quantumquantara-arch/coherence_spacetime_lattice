from __future__ import annotations
import numpy as np

def gaussian_2d(H,W,dx, sigma0):
    y,x = np.indices((H,W))
    cy,cx = (H-1)/2.0,(W-1)/2.0
    r2 = ((y-cy)*dx)**2 + ((x-cx)*dx)**2
    u = np.exp(-r2/(2*sigma0**2))
    u /= np.sum(u)
    return u

def variance(u, dx):
    H,W = u.shape
    y,x = np.indices((H,W))
    cy,cx = (H-1)/2.0,(W-1)/2.0
    r2 = ((y-cy)*dx)**2 + ((x-cx)*dx)**2
    return float(np.sum(r2*u)/np.sum(u))

def analytic_variance(D, t):
    # For 2D diffusion of a narrow Gaussian: var(t) = var(0) + 4 D t (in r^2),
    # since each coordinate variance increases by 2Dt -> r^2 adds 4Dt.
    return 4.0*D*t
