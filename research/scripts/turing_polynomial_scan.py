from __future__ import annotations

import numpy as np
import csv
from typing import Tuple

# Given a numerical Jacobian J at equilibrium and diagonal D, compute polynomials a1,a2,a3,H
# and find positive roots where RH conditions fail.

def principal_minor_sum(A: np.ndarray) -> float:
    # sum of principal 2x2 minors
    m11 = A[1,1]*A[2,2] - A[1,2]*A[2,1]
    m22 = A[0,0]*A[2,2] - A[0,2]*A[2,0]
    m33 = A[0,0]*A[1,1] - A[0,1]*A[1,0]
    return float(m11 + m22 + m33)

def cofactors_diag(J: np.ndarray) -> Tuple[float,float,float]:
    M11 = J[1,1]*J[2,2] - J[1,2]*J[2,1]
    M22 = J[0,0]*J[2,2] - J[0,2]*J[2,0]
    M33 = J[0,0]*J[1,1] - J[0,1]*J[1,0]
    return float(M11), float(M22), float(M33)

def rh_polys(J: np.ndarray, Ddiag: Tuple[float,float,float]):
    Dk, Dt, Ds = map(float, Ddiag)
    T0 = float(np.trace(J))
    S0 = principal_minor_sum(J)
    detJ = float(np.linalg.det(J))
    TrD = Dk + Dt + Ds
    SDJ = Dk*(J[1,1]+J[2,2]) + Dt*(J[0,0]+J[2,2]) + Ds*(J[0,0]+J[1,1])
    SDD = Dk*Dt + Dk*Ds + Dt*Ds
    M11, M22, M33 = cofactors_diag(J)
    C1 = Dk*M11 + Dt*M22 + Ds*M33
    C2 = Dk*Dt*J[2,2] + Dk*Ds*J[1,1] + Dt*Ds*J[0,0]
    detD = Dk*Dt*Ds

    # a1(μ)= -tr(J-μD) = -T0 + μ TrD
    # a2(μ)= S0 - μ SDJ + μ^2 SDD
    # a3(μ)= -det(J-μD)= -detJ + μ C1 - μ^2 C2 + μ^3 detD
    def a1(mu): return (-T0) + mu*TrD
    def a2(mu): return S0 - mu*SDJ + (mu*mu)*SDD
    def a3(mu): return (-detJ) + mu*C1 - (mu*mu)*C2 + (mu**3)*detD
    def H(mu): return a1(mu)*a2(mu) - a3(mu)

    return a1,a2,a3,H

def classify(J: np.ndarray, Ddiag: Tuple[float,float,float], mu_grid: np.ndarray):
    a1,a2,a3,H = rh_polys(J,Ddiag)
    # stable at mu if RH all satisfied
    def stable(mu):
        return (a1(mu)>0) and (a2(mu)>0) and (a3(mu)>0) and (H(mu)>0)
    st0 = stable(0.0)
    any_unstable = False
    mu_crit = None
    for mu in mu_grid[1:]:
        if not stable(float(mu)):
            any_unstable = True
            mu_crit = float(mu)
            break
    if not st0:
        return {"class":"hom_unstable","mu_crit":mu_crit}
    if any_unstable:
        return {"class":"turing_unstable","mu_crit":mu_crit}
    return {"class":"stable","mu_crit":None}

def main():
    # Example hook: replace with your numeric J and D from your equilibrium solver
    J = np.array([
        [-0.4, 0.2, -0.1],
        [0.15, -0.35, -0.05],
        [0.10, -0.20, -0.50],
    ], dtype=float)
    Ddiag = (0.15, 0.05, 0.10)
    mu_grid = np.linspace(0.0, 9.0, 2000)
    print(classify(J, Ddiag, mu_grid))

if __name__ == "__main__":
    main()
