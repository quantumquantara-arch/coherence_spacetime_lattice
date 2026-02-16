import numpy as np
import matplotlib.pyplot as plt
from symbolic.sympy_engine import equilibrium_numeric, jacobian_numeric

def main():
    ak_vals = np.linspace(0.1,2.0,200)
    kappas=[]
    stabilities=[]
    guess=(0.5,0.5,0.1)

    for a in ak_vals:
        params={"ak":a,"lk":0.8,"at":0.8,"lt":0.6,"as":0.7,"ls":0.5}
        eq = equilibrium_numeric(params,guess)
        guess=eq
        kappas.append(eq[0])
        J = jacobian_numeric(params,eq)
        stabilities.append(max(np.real(np.linalg.eigvals(J))))

    plt.plot(ak_vals,kappas)
    plt.show()

if __name__=="__main__":
    main()
