import numpy as np
import matplotlib.pyplot as plt

def main():
    k = np.linspace(0,1,30)
    t = np.linspace(0,1,30)
    K,T=np.meshgrid(k,t)

    ak=1; lk=0.8; at=0.8; lt=0.6; as_=0.7; ls=0.5
    S=0.2

    dK = ak*T*K*(1-K)-lk*S*K
    dT = at*K*(1-T)*(1-S)-lt*S*T

    plt.quiver(K,T,dK,dT)
    plt.show()

if __name__=="__main__":
    main()
