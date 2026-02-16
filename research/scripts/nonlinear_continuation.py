from __future__ import annotations

import math
import csv
from dataclasses import dataclass
from typing import Callable, Dict, Tuple, List, Optional

import numpy as np

# State U = (kappa, tau, sigma); parameter p = a_kappa by default

@dataclass(frozen=True)
class Params:
    Dk: float = 0.15
    Dt: float = 0.05
    Ds: float = 0.10
    ak: float = 1.00
    lk: float = 0.80
    at: float = 0.80
    lt: float = 0.60
    aS: float = 0.70
    lS: float = 0.50


def F(U: np.ndarray, p: Params) -> np.ndarray:
    k, t, s = float(U[0]), float(U[1]), float(U[2])
    # homogeneous ODE reactions (no diffusion)
    Fk = p.ak * t * k * (1.0 - k) - p.lk * s * k
    Ft = p.at * k * (1.0 - t) * (1.0 - s) - p.lt * s * t
    Fs = p.aS * (1.0 - t) * k - p.lS * s
    return np.array([Fk, Ft, Fs], dtype=float)


def fd_jacobian(fun: Callable[[np.ndarray], np.ndarray], x: np.ndarray, eps: float = 1e-7) -> np.ndarray:
    x = np.array(x, dtype=float)
    f0 = fun(x)
    J = np.zeros((f0.size, x.size), dtype=float)
    for j in range(x.size):
        xp = x.copy()
        xp[j] += eps
        fp = fun(xp)
        J[:, j] = (fp - f0) / eps
    return J


def newton_solve(fun: Callable[[np.ndarray], np.ndarray],
                 x0: np.ndarray,
                 max_iter: int = 50,
                 tol: float = 1e-10) -> np.ndarray:
    x = np.array(x0, dtype=float)
    for _ in range(max_iter):
        fx = fun(x)
        nrm = float(np.linalg.norm(fx))
        if nrm < tol:
            return x
        J = fd_jacobian(fun, x)
        try:
            step = np.linalg.solve(J, -fx)
        except np.linalg.LinAlgError:
            step = -fx
        # damping
        x = x + 0.5 * step
    return x


def pseudo_arclength_continue(
    p0: Params,
    p1: Params,
    U0: np.ndarray,
    U1: np.ndarray,
    steps: int = 200,
    ds: float = 0.02,
    param_name: str = "ak",
    max_newton: int = 40,
    tol: float = 1e-10,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Pseudo-arclength continuation of equilibria for F(U,p)=0 along a 1D branch.

    Inputs:
      - (U0,p0), (U1,p1) are two converged equilibria at nearby parameter values.
      - ds is arclength step size in augmented space (U, param).
    Outputs:
      - P array: parameter values
      - U array: equilibria, shape (N,3)

    Works through folds (saddle-nodes) if initial tangent is correct.
    """

    # build initial tangent in augmented space
    p0v = float(getattr(p0, param_name))
    p1v = float(getattr(p1, param_name))
    V0 = np.concatenate([U0, [p0v]])
    V1 = np.concatenate([U1, [p1v]])
    T = V1 - V0
    T = T / (np.linalg.norm(T) + 1e-18)

    outU: List[np.ndarray] = [U0.copy(), U1.copy()]
    outP: List[float] = [p0v, p1v]

    V_prev = V1.copy()
    T_prev = T.copy()

    for _ in range(steps):
        # predictor
        V_pred = V_prev + ds * T_prev
        U_pred = V_pred[:3]
        p_pred = float(V_pred[3])

        # corrector: solve augmented system G(V)=0:
        #   F(U,p)=0 (3 eqns)
        #   arclength constraint: (V - V_pred)·T_prev = 0 (1 eqn)
        def G(V: np.ndarray) -> np.ndarray:
            U = V[:3]
            pv = float(V[3])
            p = replace_param(p1, param_name, pv)
            g1 = F(U, p)
            g2 = np.array([np.dot(V - V_pred, T_prev)], dtype=float)
            return np.concatenate([g1, g2])

        V = np.concatenate([U_pred, [p_pred]])
        V = newton_solve(G, V, max_iter=max_newton, tol=tol)

        U_new = V[:3].copy()
        p_new = float(V[3])

        # update tangent using secant between last two points in augmented space
        T_new = V - V_prev
        T_new = T_new / (np.linalg.norm(T_new) + 1e-18)

        # store
        outU.append(U_new)
        outP.append(p_new)

        V_prev = V
        T_prev = T_new

    return np.array(outP, dtype=float), np.array(outU, dtype=float)


def replace_param(p: Params, name: str, value: float) -> Params:
    d = p.__dict__.copy()
    d[name] = float(value)
    return Params(**d)


def stability_max_real_eig(U: np.ndarray, p: Params) -> float:
    # numerical Jacobian of F at equilibrium
    fun = lambda x: F(x, p)
    J = fd_jacobian(fun, U)
    w = np.linalg.eigvals(J)
    return float(np.max(np.real(w)))


def main():
    # Two nearby equilibria to seed continuation
    base = Params()
    pA = replace_param(base, "ak", 0.40)
    pB = replace_param(base, "ak", 0.42)

    U_guess = np.array([0.4, 0.6, 0.2], dtype=float)
    U_A = newton_solve(lambda U: F(U, pA), U_guess)
    U_B = newton_solve(lambda U: F(U, pB), U_A)

    P, U = pseudo_arclength_continue(pA, pB, U_A, U_B, steps=240, ds=0.02, param_name="ak")

    # write CSV for plotting elsewhere
    with open("continuation_branch.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ak", "kappa", "tau", "sigma", "maxReEig"])
        for pv, uv in zip(P, U):
            p = replace_param(base, "ak", pv)
            m = stability_max_real_eig(uv, p)
            w.writerow([pv, float(uv[0]), float(uv[1]), float(uv[2]), m])


if __name__ == "__main__":
    main()
