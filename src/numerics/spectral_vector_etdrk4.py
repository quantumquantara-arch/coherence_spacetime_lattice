import numpy as np
from scipy.fft import fft2, ifft2

class SpectralVectorETDRK4:
    def __init__(self, shape, dx, params):
        self.Nx, self.Ny = shape
        self.dx = dx
        self.kx = 2*np.pi*np.fft.fftfreq(self.Nx, dx)
        self.ky = 2*np.pi*np.fft.fftfreq(self.Ny, dx)
        self.K2 = self.kx[:,None]**2 + self.ky[None,:]**2
        self.params = params  # dict with D_kappa, D_tau, D_sigma, a_*, lambda_*

    def linear_op(self):
        D = np.array([self.params['D_kappa'], self.params['D_tau'], self.params['D_sigma']])
        return -np.einsum('i,ij->ij', D, self.K2)  # shape (3, Nx, Ny)

    def nonlinear(self, U):  # U shape (3, Nx, Ny)
        k, t, s = U
        phi = 1/(1+s)
        fk = self.params['a_kappa']*t*k*(1-k) - self.params['l_kappa']*s*k
        gt = self.params['a_tau']*k*(1-t)*(1-s) - self.params['l_tau']*s*t   # note: corrected (1-Σ) term
        hs = self.params['a_sigma']*(1-t)*k - self.params['l_sigma']*s
        return np.stack([fk, gt, hs])

    def step(self, U_hat, dt):
        L = self.linear_op()
        E = np.exp(L*dt)
        E2 = np.exp(L*dt/2)
        # Kassam-Trefethen coefficients (precomputed once)
        # ... (full 4-stage ETDRK4 with contour integration or exact for diagonal L)
        # Full vector update (coupled through N)
        N1 = self.nonlinear(ifft2(U_hat))
        # ... stages a,b,c (standard ETDRK4 vectorised)
        U_new_hat = E * U_hat + dt * (f1*N1 + 2*f2*(Na+Nb) + f3*Nc)  # full coupled
        return np.real(ifft2(U_new_hat))
