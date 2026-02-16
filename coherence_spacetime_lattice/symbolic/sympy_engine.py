import sympy as sp
import numpy as np

k, t, s = sp.symbols("k t s", real=True)

Dk, Dt, Ds = sp.symbols("Dk Dt Ds")
ak, lk = sp.symbols("ak lk")
at, lt = sp.symbols("at lt")
as_, ls = sp.symbols("as ls")

Fk = ak*t*k*(1-k) - lk*s*k
Ft = at*k*(1-t)*(1-s) - lt*s*t
Fs = as_*(1-t)*k - ls*s

F = sp.Matrix([Fk, Ft, Fs])
J = F.jacobian([k,t,s])

def equilibrium_numeric(params, guess=(0.5,0.5,0.1)):
    subs = {
        ak:params["ak"], lk:params["lk"],
        at:params["at"], lt:params["lt"],
        as_:params["as"], ls:params["ls"]
    }
    f = sp.lambdify((k,t,s), F.subs(subs), "numpy")

    x = np.array(guess)
    for _ in range(50):
        eps = 1e-6
        Jn = np.zeros((3,3))
        fx = np.array(f(*x), dtype=float).flatten()
        for i in range(3):
            xp = x.copy()
            xp[i]+=eps
            fp = np.array(f(*xp), dtype=float).flatten()
            Jn[:,i]=(fp-fx)/eps
        x = x - 0.5*np.linalg.solve(Jn,fx)
    return x

def jacobian_numeric(params, point):
    subs = {
        ak:params["ak"], lk:params["lk"],
        at:params["at"], lt:params["lt"],
        as_:params["as"], ls:params["ls"],
        k:point[0], t:point[1], s:point[2]
    }
    return np.array(J.subs(subs), dtype=float)
