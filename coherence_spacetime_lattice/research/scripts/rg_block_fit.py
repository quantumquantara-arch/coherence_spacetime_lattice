from __future__ import annotations

import numpy as np

# Minimal block-average + least-squares parameter fit scaffold.
# You supply:
#   - simulate_fine(params) -> fields over time at fine resolution
#   - simulate_coarse(params) -> fields over time at coarse resolution
# and a parameterization vector theta.

def block_average(U: np.ndarray, b: int) -> np.ndarray:
    """
    U shape (T,H,W,C). Returns (T,H/b,W/b,C) by bxb mean pooling.
    """
    T,H,W,C = U.shape
    Hb = H//b
    Wb = W//b
    U = U[:, :Hb*b, :Wb*b, :]
    U = U.reshape(T, Hb, b, Wb, b, C).mean(axis=(2,4))
    return U

def fit_theta(U_target: np.ndarray, simulator, theta0: np.ndarray, steps: int = 60, lr: float = 0.1) -> np.ndarray:
    """
    Finite-difference gradient descent minimizing ||sim(theta)-U_target||_2.
    """
    theta = theta0.astype(float).copy()
    for _ in range(steps):
        U_pred = simulator(theta)
        loss = float(np.mean((U_pred - U_target)**2))

        grad = np.zeros_like(theta)
        eps = 1e-4
        for i in range(theta.size):
            tp = theta.copy()
            tp[i] += eps
            Up = simulator(tp)
            lp = float(np.mean((Up - U_target)**2))
            grad[i] = (lp - loss) / eps

        theta = theta - lr * grad
    return theta
