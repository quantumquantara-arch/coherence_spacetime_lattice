from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from symbolic.complex_amplitude_engine import ComplexParams, step_complex_system

def main():
    H,W = 128,128
    dx = 1.0
    dt = 0.02
    p = ComplexParams()

    y,x = np.indices((H,W))
    cy,cx = H//2, W//2
    r2 = (y-cy)**2 + (x-cx)**2
    psi = np.exp(-r2/(2*9.0)).astype(np.complex128) * np.exp(1j*0.2*x)
    tau = np.zeros((H,W), dtype=float)
    sigma = np.zeros((H,W), dtype=float)
    tau[H//2-5:H//2+5, W//2-5:W//2+5] = 1.0

    for _ in range(400):
        psi, tau, sigma = step_complex_system(psi, tau, sigma, p, dt=dt, dx=dx)

    kappa = np.abs(psi)**2

    plt.figure(figsize=(12,4))
    plt.subplot(1,3,1); plt.imshow(kappa, origin="lower"); plt.title("|psi|^2 = kappa"); plt.colorbar()
    plt.subplot(1,3,2); plt.imshow(tau, origin="lower"); plt.title("tau"); plt.colorbar()
    plt.subplot(1,3,3); plt.imshow(sigma, origin="lower"); plt.title("sigma"); plt.colorbar()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
