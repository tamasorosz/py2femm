# Tangential force %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

resA_T2 = []
resA_T1 = []

# Inputs
r = 22.25/1000      # radius [m]
l = 40/1000       # stack length [m]

dfArr = pd.read_csv('caseAr_right.csv')
dfAtr = pd.read_csv('caseAt_right.csv')

for i in range(len(dfArr.columns)):
    # Example: tangential stress list (in Pa)
    pt = [Ar*At for Ar, At in zip(dfArr.iloc[:,i], dfAtr.iloc[:,i])]

    pt_t2 = pt[:1937]
    pt_t1 = pt[1937:]

    # Number of samples
    Nt2 = len(pt_t2)
    Nt1 = len(pt_t1)

    # Create angular positions
    theta_t2 = np.linspace(0, np.radians(28.71), Nt2, endpoint=False)
    theta_t1 = np.linspace(0, np.radians(14.86), Nt1, endpoint=False)

    # Convert pt list to numpy array
    pt_t2 = np.array(pt_t2)
    pt_t1 = np.array(pt_t1)

    # Numerical integration using trapezoidal rule
    Ft_t2 = -1 * r * l / (4*np.pi*1e-7) * np.trapz(pt_t2, theta_t2)
    Ft_t1 = r * l / (4*np.pi*1e-7) * np.trapz(pt_t1, theta_t1)

    resA_T2.append(Ft_t2)
    resA_T1.append(Ft_t1)

dAT1 = np.gradient(resA_T2, np.linspace(0, 7.5, 16))
dAT2 = np.gradient(resA_T1, np.linspace(0, 7.5, 16))
plt.plot(resA_T2)
plt.plot(resA_T1)
plt.show()
plt.plot(dAT2)
plt.plot(dAT1)
plt.show()