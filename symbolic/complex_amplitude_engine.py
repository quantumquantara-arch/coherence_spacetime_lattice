from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Optional, Dict

import numpy as np

"""
Complex-amplitude coupling: introduce psi = A exp(i theta), with kappa = |psi|^2.
Core idea:
- psi evolves by a dissipative + dispersive PDE (complex Ginzburg–Landau / NLS hybrid)
- tau and sigma evolve as real fields coupled to kappa=|psi|^2

This provides a bridge to mainstream quantum-style complex amplitudes while preserving
the coherence-first variables.

Equation set (dimensionless):
  ∂t psi = i c0 ∇² psi - i g |psi|^2 psi  +  (eta * tau) psi (1-|psi|^2)  -  gamma(sigma) psi
  ∂t tau = D_tau ∇² tau + a_tau |psi|^2 (1-tau)(1-sigma) - lambda_tau sigma tau
  ∂t sigma = D_sigma ∇² sigma + a_sigma (1-tau)|psi|^2 - lambda_sigma sigma

gamma(sigma) = gamma0 + gamma1 sigma  (decoherence/damping by separation load)
"""

@dataclass(frozen=True)
class ComplexParams:
    # psi dynamics
    c0: float = 0.35      # dispersion strength (Schrodinger-like)
    g: float = 0.70       # nonlinear phase shift
    eta: float = 1.00     # logistic coherence pumping gated by tau
    gamma0: float = 0.05
    gamma1: float = 0.40

    # tau,sigma diffusion + reactions
    D_tau: float = 0.05
    D_sigma: float = 0.10
    a_tau: float = 0.80
    lambda_tau: float = 0.60
    a_sigma: float = 0.70
    lambda_sigma: float = 0.50


def laplacian_5pt(u: np.ndarray) -> np.ndarray:
    up = np.pad(u, ((1, 1), (1, 1)), mode="edge")
    c = up[1:-1, 1:-1]
    n = up[:-2, 1:-1]
    s = up[2:, 1:-1]
    w = up[1:-1, :-2]
    e = up[1:-1, 2:]
    return (n + s + w + e - 4.0 * c)


def step_complex_system(
    psi: np.ndarray,
    tau: np.ndarray,
    sigma: np.ndarray,
    p: ComplexParams,
    dt: float,
    dx: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    kappa = np.abs(psi) ** 2

    lap_psi = laplacian_5pt(psi) / (dx * dx)
    lap_tau = laplacian_5pt(tau) / (dx * dx)
    lap_sig = laplacian_5pt(sigma) / (dx * dx)

    gamma = p.gamma0 + p.gamma1 * sigma

    dpsi = (1j * p.c0 * lap_psi) - (1j * p.g * kappa * psi) + (p.eta * tau) * psi * (1.0 - kappa) - gamma * psi
    dtau = p.D_tau * lap_tau + p.a_tau * kappa * (1.0 - tau) * (1.0 - sigma) - p.lambda_tau * sigma * tau
    dsig = p.D_sigma * lap_sig + p.a_sigma * (1.0 - tau) * kappa - p.lambda_sigma * sigma

    psi_new = psi + dt * dpsi
    tau_new = np.clip(tau + dt * dtau, 0.0, 1.0)
    sig_new = np.maximum(sigma + dt * dsig, 0.0)

    return psi_new, tau_new, sig_new


def energy_like_functional(
    psi: np.ndarray,
    tau: np.ndarray,
    sigma: np.ndarray,
    p: ComplexParams,
    dx: float = 1.0,
    eps: float = 1e-12,
) -> float:
    """
    Not a conserved Hamiltonian in the full dissipative model.
    Useful diagnostic combining gradient energy + local potentials.

    E = ∫ [ c0 |∇psi|^2 + (g/2)|psi|^4  + 0.5|∇tau|^2 + 0.5|∇sigma|^2
            + sigma^2/2 - eta tau |psi|^2 + eta tau |psi|^4/2 ] dx
    """
    kappa = np.abs(psi) ** 2

    psix = np.diff(np.pad(psi, ((0, 0), (0, 1)), mode="edge"), axis=1)
    psiy = np.diff(np.pad(psi, ((0, 1), (0, 0)), mode="edge"), axis=0)
    taux = np.diff(np.pad(tau, ((0, 0), (0, 1)), mode="edge"), axis=1)
    tauy = np.diff(np.pad(tau, ((0, 1), (0, 0)), mode="edge"), axis=0)
    sigx = np.diff(np.pad(sigma, ((0, 0), (0, 1)), mode="edge"), axis=1)
    sigy = np.diff(np.pad(sigma, ((0, 1), (0, 0)), mode="edge"), axis=0)

    grad = p.c0 * (np.abs(psix) ** 2 + np.abs(psiy) ** 2) + 0.5 * (taux**2 + tauy**2) + 0.5 * (sigx**2 + sigy**2)
    local = 0.5 * (p.g * kappa**2) + 0.5 * (sigma**2) - p.eta * tau * kappa + 0.5 * p.eta * tau * kappa**2
    return float(np.sum(grad + local) * (dx * dx))
