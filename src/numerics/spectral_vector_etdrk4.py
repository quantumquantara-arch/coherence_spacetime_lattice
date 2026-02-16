from __future__ import annotations
import numpy as np

def make_K2(ny: int, nx: int, Lx: float = 1.0, Ly: float = 1.0) -> np.ndarray:
    kx = 2*np.pi*np.fft.fftfreq(nx, d=Lx/nx)
    ky = 2*np.pi*np.fft.fftfreq(ny, d=Ly/ny)
    KX, KY = np.meshgrid(kx, ky)
    return KX**2 + KY**2

def etdrk4_coeffs(L: np.ndarray, dt: float, M: int = 16):
    # Cox–Matthews with Kassam–Trefethen contour averaging
    E  = np.exp(dt*L)
    E2 = np.exp(dt*L/2.0)
    r = np.exp(1j*np.pi*(np.arange(1, M+1)-0.5)/M)
    LR = dt*L[..., None] + r
    Q  = dt*np.real(np.mean((np.exp(LR/2.0)-1.0)/LR, axis=-1))
    f1 = dt*np.real(np.mean((-4-LR+np.exp(LR)*(4-3*LR+LR**2))/LR**3, axis=-1))
    f2 = dt*np.real(np.mean((2+LR+np.exp(LR)*(-2+LR))/LR**3, axis=-1))
    f3 = dt*np.real(np.mean((-4-3*LR-LR**2+np.exp(LR)*(4-LR))/LR**3, axis=-1))
    return E, E2, Q, f1, f2, f3

def phi_sigma(sigma: np.ndarray) -> np.ndarray:
    return 1.0/(1.0 + sigma)

def N_rhs(k: np.ndarray, t: np.ndarray, s: np.ndarray, p: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    fk = p["ak"]*t*k*(1.0-k) - p["lk"]*s*k
    gt = p["at"]*k*(1.0-t)*phi_sigma(s) - p["lt"]*s*t
    hs = p["aS"]*(1.0-t)*k - p["lS"]*s
    return fk, gt, hs

def step_vector_etdrk4(kappa, tau, sigma, p, dt, K2):
    # Linear operators per field in Fourier space
    Lk = -p["Dk"]*K2
    Lt = -p["Dt"]*K2
    Ls = -p["Ds"]*K2
    Ek,Ek2,Qk,f1k,f2k,f3k = etdrk4_coeffs(Lk, dt)
    Et,Et2,Qt,f1t,f2t,f3t = etdrk4_coeffs(Lt, dt)
    Es,Es2,Qs,f1s,f2s,f3s = etdrk4_coeffs(Ls, dt)

    # FFT state
    kh = np.fft.fft2(kappa)
    th = np.fft.fft2(tau)
    sh = np.fft.fft2(sigma)

    # Stage 0 nonlinear
    fk, gt, hs = N_rhs(kappa, tau, sigma, p)
    Fk = np.fft.fft2(fk); Gt = np.fft.fft2(gt); Hs = np.fft.fft2(hs)

    # a
    ka = Ek2*kh + Qk*Fk
    ta = Et2*th + Qt*Gt
    sa = Es2*sh + Qs*Hs
    k_a = np.real(np.fft.ifft2(ka)); t_a = np.real(np.fft.ifft2(ta)); s_a = np.real(np.fft.ifft2(sa))
    fk_a, gt_a, hs_a = N_rhs(k_a, t_a, s_a, p)
    Fk_a = np.fft.fft2(fk_a); Gt_a = np.fft.fft2(gt_a); Hs_a = np.fft.fft2(hs_a)

    # b
    kb = Ek2*kh + Qk*Fk_a
    tb = Et2*th + Qt*Gt_a
    sb = Es2*sh + Qs*Hs_a
    k_b = np.real(np.fft.ifft2(kb)); t_b = np.real(np.fft.ifft2(tb)); s_b = np.real(np.fft.ifft2(sb))
    fk_b, gt_b, hs_b = N_rhs(k_b, t_b, s_b, p)
    Fk_b = np.fft.fft2(fk_b); Gt_b = np.fft.fft2(gt_b); Hs_b = np.fft.fft2(hs_b)

    # c
    kc = Ek2*ka + Qk*(2.0*Fk_b - Fk)
    tc = Et2*ta + Qt*(2.0*Gt_b - Gt)
    sc = Es2*sa + Qs*(2.0*Hs_b - Hs)
    k_c = np.real(np.fft.ifft2(kc)); t_c = np.real(np.fft.ifft2(tc)); s_c = np.real(np.fft.ifft2(sc))
    fk_c, gt_c, hs_c = N_rhs(k_c, t_c, s_c, p)
    Fk_c = np.fft.fft2(fk_c); Gt_c = np.fft.fft2(gt_c); Hs_c = np.fft.fft2(hs_c)

    # Combine
    kh_new = Ek*kh + f1k*Fk + 2.0*f2k*(Fk_a+Fk_b) + f3k*Fk_c
    th_new = Et*th + f1t*Gt + 2.0*f2t*(Gt_a+Gt_b) + f3t*Gt_c
    sh_new = Es*sh + f1s*Hs + 2.0*f2s*(Hs_a+Hs_b) + f3s*Hs_c

    k_new = np.real(np.fft.ifft2(kh_new))
    t_new = np.real(np.fft.ifft2(th_new))
    s_new = np.real(np.fft.ifft2(sh_new))

    # invariant-region guardrail
    k_new = np.clip(k_new, 0.0, 1.0)
    t_new = np.clip(t_new, 0.0, 1.0)
    s_new = np.maximum(s_new, 0.0)
    return k_new, t_new, s_new
