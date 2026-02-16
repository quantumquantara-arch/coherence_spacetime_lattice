"""
coherence_field.py

Research-grade toy model (explicitly non-Standard-Model) for a κ–τ–Σ field on a 2D lattice.

State variables (dimensionless, default bounds):
  κ(y,x) ∈ [0,1]  : coherence density (proxy for local phase-locked order / purity-like resource)
  τ(y,x) ∈ [0,1]  : temporal responsibility (stability / continuity bias)
  Σ(y,x) ∈ [0,∞)  : systemic separation (fragmentation / hidden entropy-like load)

Continuous-form target PDE (reaction–diffusion with saturations):
  ∂t κ = Dκ ∇²κ + fκ(κ,τ,Σ)
  ∂t τ = Dτ ∇²τ + fτ(κ,τ,Σ)
  ∂t Σ = DΣ ∇²Σ + fΣ(κ,τ,Σ)

Discretization:
  - 5-point Laplacian (reflecting / Neumann boundaries by edge padding)
  - forward Euler in time (with a conservative dt stability check for diffusion)

Notes:
  - This module is designed to be testable, numerically stable under reasonable dt,
    and extensible toward more formal derivations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, Literal

import numpy as np

BoundaryMode = Literal["reflect"]


@dataclass(frozen=True)
class CoherenceMetrics:
    kappa: float
    tau: float
    sigma: float

    def as_array(self) -> np.ndarray:
        return np.array([self.kappa, self.tau, self.sigma], dtype=float)


@dataclass(frozen=True)
class CoherenceParams:
    # diffusion coefficients (dimensionless)
    D_kappa: float = 0.15
    D_tau: float = 0.05
    D_sigma: float = 0.10

    # reaction parameters (dimensionless)
    # κ production: logistic growth gated by τ and penalized by Σ
    a_kappa: float = 1.00
    lambda_kappa: float = 0.80

    # τ reinforcement: increases when κ high and Σ low; decays under Σ
    a_tau: float = 0.80
    lambda_tau: float = 0.60

    # Σ production: rises when τ low and κ present; decays intrinsically
    a_sigma: float = 0.70
    lambda_sigma: float = 0.50

    # optional nonlinearities / couplings
    tau_gate_power: float = 1.0
    sigma_penalty_power: float = 1.0

    # numerical bounds
    kappa_clip: Tuple[float, float] = (0.0, 1.0)
    tau_clip: Tuple[float, float] = (0.0, 1.0)
    sigma_floor: float = 0.0


def _laplacian_5pt(u: np.ndarray, boundary: BoundaryMode = "reflect") -> np.ndarray:
    """
    2D 5-point Laplacian with Neumann-like reflecting boundaries via padding.
    """
    if boundary != "reflect":
        raise ValueError(f"Unsupported boundary mode: {boundary}")

    up = np.pad(u, ((1, 1), (1, 1)), mode="edge")
    c = up[1:-1, 1:-1]
    n = up[:-2, 1:-1]
    s = up[2:, 1:-1]
    w = up[1:-1, :-2]
    e = up[1:-1, 2:]
    return (n + s + w + e - 4.0 * c)


def _stable_dt_for_diffusion(dx: float, D_max: float, safety: float = 0.90) -> float:
    """
    Conservative explicit stability condition in 2D for 5-point Laplacian:
      dt <= dx^2 / (4 D_max)
    """
    if D_max <= 0:
        return np.inf
    return safety * (dx * dx) / (4.0 * D_max)


class CoherenceField:
    """
    Stores κ, τ, Σ on a 2D lattice and advances them by a reaction–diffusion step.
    """

    def __init__(
        self,
        height: int,
        width: int,
        *,
        dx: float = 1.0,
        params: Optional[CoherenceParams] = None,
        boundary: BoundaryMode = "reflect",
        dtype: np.dtype = np.float64,
    ):
        self.height = int(height)
        self.width = int(width)
        self.dx = float(dx)
        self.params = params or CoherenceParams()
        self.boundary = boundary
        self._field = np.zeros((self.height, self.width, 3), dtype=dtype)

    # --- array views (kept for compatibility with existing tests) ---
    @property
    def kappa(self) -> np.ndarray:
        return self._field[:, :, 0]

    @property
    def tau(self) -> np.ndarray:
        return self._field[:, :, 1]

    @property
    def sigma(self) -> np.ndarray:
        return self._field[:, :, 2]

    # --- pointwise helpers ---
    def get_metrics(self, y: int, x: int) -> CoherenceMetrics:
        k, t, s = self._field[int(y), int(x), :]
        return CoherenceMetrics(float(k), float(t), float(s))

    def set_metrics(self, y: int, x: int, metrics: CoherenceMetrics) -> None:
        self._field[int(y), int(x), :] = metrics.as_array()

    def neighborhood_average(self, y: int, x: int) -> CoherenceMetrics:
        y = int(y)
        x = int(x)
        ys = max(0, y - 1)
        ye = min(self.height, y + 2)
        xs = max(0, x - 1)
        xe = min(self.width, x + 2)
        patch = self._field[ys:ye, xs:xe, :]
        avg = np.mean(patch, axis=(0, 1))
        return CoherenceMetrics(float(avg[0]), float(avg[1]), float(avg[2]))

    # --- initialization ---
    def randomize(
        self,
        kappa_range: Tuple[float, float] = (0.0, 0.2),
        tau_range: Tuple[float, float] = (0.0, 0.2),
        sigma_range: Tuple[float, float] = (0.0, 0.2),
        seed: Optional[int] = None,
    ) -> None:
        rng = np.random.default_rng(seed)
        self.kappa[:, :] = rng.uniform(*kappa_range, size=(self.height, self.width))
        self.tau[:, :] = rng.uniform(*tau_range, size=(self.height, self.width))
        self.sigma[:, :] = rng.uniform(*sigma_range, size=(self.height, self.width))
        self._apply_bounds_inplace()

    def initialize_center_pulse(
        self,
        *,
        kappa_peak: float = 1.0,
        radius: int = 3,
        tau_value: float = 1.0,
        sigma_value: float = 0.0,
    ) -> None:
        cy, cx = self.height // 2, self.width // 2
        rr = int(radius) * int(radius)
        y = np.arange(self.height)[:, None]
        x = np.arange(self.width)[None, :]
        mask = (y - cy) ** 2 + (x - cx) ** 2 <= rr
        self.kappa[mask] = float(kappa_peak)
        self.tau[mask] = float(tau_value)
        self.sigma[mask] = float(sigma_value)
        self._apply_bounds_inplace()

    # --- dynamics ---
    def _reaction_terms(self, k: np.ndarray, t: np.ndarray, s: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        p = self.params

        # gates
        tau_gate = np.power(np.clip(t, 0.0, 1.0), p.tau_gate_power)
        sigma_penalty = np.power(np.maximum(s, 0.0), p.sigma_penalty_power)

        # κ: logistic growth gated by τ, suppressed by Σ load
        f_k = p.a_kappa * tau_gate * k * (1.0 - k) - p.lambda_kappa * sigma_penalty * k

        # τ: reinforced by κ when Σ low; decays under Σ
        f_t = p.a_tau * k * (1.0 - np.clip(s, 0.0, 1.0)) * (1.0 - t) - p.lambda_tau * sigma_penalty * t

        # Σ: produced when τ low but κ present; decays intrinsically
        f_s = p.a_sigma * (1.0 - t) * k - p.lambda_sigma * s

        return f_k, f_t, f_s

    def step_local_dynamics(
        self,
        *,
        dt: Optional[float] = None,
        noise_std: float = 0.0,
        seed: Optional[int] = None,
    ) -> None:
        """
        Advance one step with explicit reaction–diffusion.

        If dt is None, chooses dt from diffusion stability bound.
        """
        p = self.params
        Dmax = max(p.D_kappa, p.D_tau, p.D_sigma)
        dt_max = _stable_dt_for_diffusion(self.dx, Dmax)
        if dt is None:
            dt = min(0.10, dt_max)  # conservative default
        else:
            dt = float(dt)
            if dt > dt_max:
                raise ValueError(f"Unstable dt for diffusion: dt={dt} > dt_max={dt_max:.6g} (dx={self.dx}, Dmax={Dmax})")

        k = self.kappa.copy()
        t = self.tau.copy()
        s = self.sigma.copy()

        lap_k = _laplacian_5pt(k, boundary=self.boundary) / (self.dx * self.dx)
        lap_t = _laplacian_5pt(t, boundary=self.boundary) / (self.dx * self.dx)
        lap_s = _laplacian_5pt(s, boundary=self.boundary) / (self.dx * self.dx)

        f_k, f_t, f_s = self._reaction_terms(k, t, s)

        k_new = k + dt * (p.D_kappa * lap_k + f_k)
        t_new = t + dt * (p.D_tau * lap_t + f_t)
        s_new = s + dt * (p.D_sigma * lap_s + f_s)

        if noise_std > 0.0:
            rng = np.random.default_rng(seed)
            k_new = k_new + rng.normal(0.0, noise_std, size=k_new.shape)
            t_new = t_new + rng.normal(0.0, noise_std, size=t_new.shape)
            s_new = s_new + rng.normal(0.0, noise_std, size=s_new.shape)

        self.kappa[:, :] = k_new
        self.tau[:, :] = t_new
        self.sigma[:, :] = s_new
        self._apply_bounds_inplace()

    def _apply_bounds_inplace(self) -> None:
        p = self.params
        k0, k1 = p.kappa_clip
        t0, t1 = p.tau_clip
        np.clip(self.kappa, k0, k1, out=self.kappa)
        np.clip(self.tau, t0, t1, out=self.tau)
        np.maximum(self.sigma, p.sigma_floor, out=self.sigma)

    # --- diagnostics ---
    def aggregate_metrics(self) -> CoherenceMetrics:
        avg = np.mean(self._field, axis=(0, 1))
        return CoherenceMetrics(kappa=float(avg[0]), tau=float(avg[1]), sigma=float(avg[2]))

    def coherence_free_energy(self, *, eps: float = 1e-12) -> float:
        """
        A toy Lyapunov-like functional (not a claim of physical free energy).
        Useful for regression tests and qualitative stability checks.

        F = ∫ [ (1/2)|∇κ|^2 + (1/2)|∇τ|^2 + (1/2)|∇Σ|^2
              + V(κ,τ,Σ) ] dA

        Potential V biases:
          - rewards κ,τ when Σ low
          - penalizes large Σ
        """
        k = self.kappa
        t = self.tau
        s = self.sigma

        # gradients via forward differences (reflecting via edge padding)
        kx = np.diff(np.pad(k, ((0, 0), (0, 1)), mode="edge"), axis=1)
        ky = np.diff(np.pad(k, ((0, 1), (0, 0)), mode="edge"), axis=0)
        tx = np.diff(np.pad(t, ((0, 0), (0, 1)), mode="edge"), axis=1)
        ty = np.diff(np.pad(t, ((0, 1), (0, 0)), mode="edge"), axis=0)
        sx = np.diff(np.pad(s, ((0, 0), (0, 1)), mode="edge"), axis=1)
        sy = np.diff(np.pad(s, ((0, 1), (0, 0)), mode="edge"), axis=0)

        grad_term = 0.5 * (kx * kx + ky * ky + tx * tx + ty * ty + sx * sx + sy * sy)

        # simple potential
        V = (1.0 - s / (1.0 + s + eps)) * (-(k + t) + (k * k + t * t)) + 0.5 * (s * s)

        return float(np.sum(grad_term + V) * (self.dx * self.dx))
