# Tangential force %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

resA_T1 = []
resA_T2 = []

# Inputs
r = 22.25/1000      # radius [m]
l = 40/1000       # stack length [m]

dfAr = pd.read_csv('caseAr_f.csv')
dfAt = pd.read_csv('caseAt_f.csv')

for i in range(len(dfAr.columns)):
    # Example: tangential stress list (in Pa)
    pt = [Ar*At for Ar, At in zip(dfAr.iloc[:,i], dfAt.iloc[:,i])]

    pt_t1 = pt[:1066]
    pt_t2 = pt[1066:]

    # Number of samples
    Nt1 = len(pt_t1)
    Nt2 = len(pt_t2)

    # Create angular positions
    theta_t1 = np.linspace(0, np.radians(14.86), Nt1, endpoint=False)
    theta_t2 = np.linspace(0, np.radians(28.71), Nt2, endpoint=False)

    # Convert pt list to numpy array
    pt_t1 = np.array(pt_t1)
    pt_t2 = np.array(pt_t2)

    # Numerical integration using trapezoidal rule
    Ft_t1 = -1 * r * l / (4*np.pi*1e-7) * np.trapezoid(pt_t1, theta_t1)
    Ft_t2 = r * l / (4*np.pi*1e-7) * np.trapezoid(pt_t2, theta_t2)

    resA_T1.append(Ft_t1)
    resA_T2.append(Ft_t2)

dAT1 = np.gradient(resA_T1, np.linspace(0, 7.5, 16))
dAT2 = np.gradient(resA_T2, np.linspace(0, 7.5, 16))
plt.plot(resA_T1)
plt.plot(resA_T2)
plt.show()
plt.plot(dAT1)
plt.plot(dAT2)
plt.show()