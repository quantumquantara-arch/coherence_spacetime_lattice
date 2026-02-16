from __future__ import annotations
import numpy as np

def make_wavenumbers(ny, nx, Lx=1.0, Ly=1.0):
    kx = 2*np.pi*np.fft.fftfreq(nx, d=Lx/nx)
    ky = 2*np.pi*np.fft.fftfreq(ny, d=Ly/ny)
    KX, KY = np.meshgrid(kx, ky)
    K2 = KX**2 + KY**2
    return K2

def etdrk4_coeffs(L, dt):
    # Cox-Matthews ETDRK4 scalar coefficients for operator L (array)
    E = np.exp(dt*L)
    E2 = np.exp(dt*L/2.0)
    M = 16
    r = np.exp(1j*np.pi*(np.arange(1,M+1)-0.5)/M)
    LR = dt*L[...,None] + r
    Q  = dt*np.real(np.mean((np.exp(LR/2.0)-1.0)/LR, axis=-1))
    f1 = dt*np.real(np.mean((-4-LR+np.exp(LR)*(4-3*LR+LR**2))/LR**3, axis=-1))
    f2 = dt*np.real(np.mean((2+LR+np.exp(LR)*(-2+LR))/LR**3, axis=-1))
    f3 = dt*np.real(np.mean((-4-3*LR-LR**2+np.exp(LR)*(4-LR))/LR**3, axis=-1))
    return E,E2,Q,f1,f2,f3

def step_etdrk4(u, D, dt, K2, nonlin):
    """
    Periodic spectral ETDRK4 for scalar u_t = D Δu + N(u).
    nonlin(u) returns N(u) in physical space.
    """
    L = -D*K2
    E,E2,Q,f1,f2,f3 = etdrk4_coeffs(L, dt)
    uh = np.fft.fft2(u)

    Nu = np.fft.fft2(nonlin(u))
    a  = E2*uh + Q*Nu
    Na = np.fft.fft2(nonlin(np.real(np.fft.ifft2(a))))
    b  = E2*uh + Q*Na
    Nb = np.fft.fft2(nonlin(np.real(np.fft.ifft2(b))))
    c  = E2*a  + Q*(2*Nb - Nu)
    Nc = np.fft.fft2(nonlin(np.real(np.fft.ifft2(c))))

    uh_new = E*uh + f1*Nu + 2*f2*(Na+Nb) + f3*Nc
    return np.real(np.fft.ifft2(uh_new))

def step_ktS_etdrk4(kappa, tau, sigma, params, dt, K2):
    """
    Full 3-field periodic ETDRK4 with safe kinetics.
    """
    def phi(s): return 1.0/(1.0+s)

    def Nk(k,t,s): return params["ak"]*t*k*(1-k) - params["lk"]*s*k
    def Nt(k,t,s): return params["at"]*k*(1-t)*phi(s) - params["lt"]*s*t
    def Ns(k,t,s): return params["aS"]*(1-t)*k - params["lS"]*s

    k = step_etdrk4(kappa, params["Dk"], dt, K2, lambda u: Nk(u,tau,sigma))
    t = step_etdrk4(tau,   params["Dt"], dt, K2, lambda u: Nt(kappa,u,sigma))
    s = step_etdrk4(sigma, params["Ds"], dt, K2, lambda u: Ns(kappa,tau,u))

    k = np.clip(k, 0.0, 1.0)
    t = np.clip(t, 0.0, 1.0)
    s = np.maximum(s, 0.0)
    return k,t,s
