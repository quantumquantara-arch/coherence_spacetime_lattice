import numpy as np
import matplotlib.pyplot as plt
from symbolic.sympy_engine import equilibrium_numeric, jacobian_numeric

def main():
    ak_vals=np.linspace(0.2,2,80)
    lk_vals=np.linspace(0.1,1.5,80)
    phase=np.zeros((80,80))

    for i,lk in enumerate(lk_vals):
        guess=(0.5,0.5,0.1)
        for j,ak in enumerate(ak_vals):
            params={"ak":ak,"lk":lk,"at":0.8,"lt":0.6,"as":0.7,"ls":0.5}
            eq=equilibrium_numeric(params,guess)
            guess=eq
            J=jacobian_numeric(params,eq)
            eig=max(np.real(np.linalg.eigvals(J)))
            phase[i,j]=eig

    plt.imshow(phase,origin="lower")
    plt.colorbar()
    plt.show()

if __name__=="__main__":
    main()
